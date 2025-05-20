import os
import logging  # 추가
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
import json

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 외부 함수 임포트
from src.fetcher.stock_data_fetcher import fetch_stock_data
from src.models.stock_predictor_model import transformer_forecast

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ 프롬프트 템플릿 정의
stock_prompt = PromptTemplate.from_template("""
당신은 금융 데이터 분석가입니다. 아래 정보를 바탕으로 주가 분석을 수행하세요:

[기업명] {company}

[예측 데이터 요약]
{text}

[작업 내용]
- 향후 1~3개월간 주가 변화 방향을 요약
- 상승/하락 추세 여부
- 예측의 근거를 설명

[출력 형식]
- 기업명: {company}
  - 주가 예측 요약: ...
  - 상승/하락 트렌드 여부: ...
  - 예측 근거 요약: ...
""")

# ✅ LLM 및 출력 파서 설정
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, openai_api_key=OPENAI_API_KEY)
output_parser = StrOutputParser()
stock_chain = stock_prompt | llm | output_parser

# ✅ 주가 예측 에이전트 함수
def predict_stock_prices(state):
    """
    주가 예측 에이전트 함수. Supervisor에서 호출되며, 배터리 3사의 데이터를 직접 처리합니다.

    Args:
        state (dict): Supervisor에서 전달받은 상태 객체

    Returns:
        dict: 업데이트된 state 객체
    """
    # 배터리 3사 목록 직접 정의
    company_list = {
        "Samsung SDI": "006400.KS",
        "LG에너지솔루션": "373220.KS",
        "동원시스템즈": "014820.KS"
    }

    logging.info(f"Processing stock data for companies: {company_list}")

    result_dict = {}
    for company, ticker in company_list.items():
        try:
            logging.info(f"Fetching stock data for {company} ({ticker})...")
            # 주가 데이터 수집
            stock_data = fetch_stock_data(company_name=company, ticker=ticker)

            logging.info(f"Stock data fetched for {company}. Starting forecast...")
            # 주가 예측
            forecast = transformer_forecast(stock_data)

            # NumPy 배열을 리스트로 변환
            forecast_list = forecast.tolist()

            # JSON 파일로 저장
            json_path = f"output/{company}_forecast.json"
            os.makedirs("output", exist_ok=True)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(forecast_list, f, ensure_ascii=False, indent=4)
            logging.info(f"Forecast JSON saved for {company} at {json_path}")

            # CSV 파일로 저장
            csv_path = f"output/{company}_forecast.csv"
            pd.DataFrame(forecast_list).to_csv(csv_path, index=False)
            logging.info(f"Forecast CSV saved for {company} at {csv_path}")

            # LLM 호출
            analysis_result = stock_chain.invoke({
                "company": company,
                "text": json.dumps(forecast_list, ensure_ascii=False)
            })

            logging.info(f"LLM analysis result for {company}: {analysis_result}")
            result_dict[company] = analysis_result

        except Exception as e:
            logging.error(f"Error analyzing {company}: {str(e)}")
            result_dict[company] = {"error": str(e)}

    # 결과를 state에 저장
    state["stock_data"] = result_dict
    logging.info("Stock price analysis completed. Results stored in state.")
    return state