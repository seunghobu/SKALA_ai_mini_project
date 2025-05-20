import logging
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv  
import os  

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ✅ 임베딩 모델 설정
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Chroma 벡터 DB 로드
vector_db = Chroma(
    persist_directory="./vectorstores/battery_db",  # 배터리 산업 관련 DB 경로로 수정하세요
    embedding_function=embeddings
)

# ✅ 배터리 산업 분석 프롬프트 정의
battery_prompt = PromptTemplate.from_template(
    """
    당신은 2차전지 및 배터리 산업 전문가입니다. 다음 작업을 수행하세요:

    [작업 내용]
    - 2025년 기준 배터리 제조 시장 현실 분석
    - "삼성SDI", "LG에너지솔루션", "동원시스템즈" 중심으로 배터리 소재 및 공급망 현황 정리
    - 배터리 제조 관련 최신 기술 트렌드 분석
    - 미국의 관세 정책에 따른 배터리 시장 영향 분석

    [출력 형식]
    - 시장 동향: ...
    - 소재/공급망: ...
    - 기술 트렌드: ...

    정보는 지난 데이터가 아닌 오직 2025년의 최신 시장 데이터와 동향을 바탕으로 간결하게 정리하세요.
    아래 검색 결과를 참고하여 내용을 작성하세요:

    --- 검색 결과 ---
    {text}
    ------------------
    """
)

# 모델 정의
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1
)

# 출력 파서 정의
output_parser = StrOutputParser()

# 체인 구성
battery_analysis_chain = battery_prompt | llm | output_parser

# ✅ 시장 분석 실행 함수
def run_battery_market_agent(state, keyword: str = "배터리 산업", top_k: int = 5):
    """
    시장 분석 에이전트 함수. Supervisor에서 호출되며, state를 통해 데이터를 전달받고 결과를 저장합니다.

    Args:
        state (dict): Supervisor에서 전달받은 상태 객체
        keyword (str): 검색 키워드
        top_k (int): 유사도 검색에서 반환할 문서 수

    Returns:
        dict: 업데이트된 state 객체
    """
    try:
        logging.info(f"Running battery market agent with keyword: {keyword}")

        # Chroma에서 유사도 기반 검색
        results = vector_db.similarity_search(keyword, k=top_k)
        content = "\n\n".join([r.page_content for r in results])

        # LLM에 전달
        result = battery_analysis_chain.invoke({"text": content})

        logging.info("Battery Market Agent completed successfully.")
        # 결과를 state에 저장
        state["market_data"] = {
            "keyword": keyword,
            "분석 결과": result
        }
    except Exception as e:
        logging.error(f"Battery Market Agent Error: {str(e)}")
        state["market_data"] = {
            "error": str(e)
        }

    return state