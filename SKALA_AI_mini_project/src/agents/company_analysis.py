import logging
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

# ✅ Chroma DB 로드 (기업별 자료 포함)
vector_db = Chroma(
    persist_directory="./vectorstores/company_db",  # DB 폴더명을 상황에 맞게 수정
    embedding_function=embeddings
)

# ✅ 분석 프롬프트 템플릿
company_prompt = PromptTemplate.from_template(
    """
    당신은 배터리 산업 전문가입니다. 아래 검색 결과를 바탕으로 **{company}**에 대한 산업적 분석을 수행하세요.
    다른 회사에 대한 정보는 포함하지 마세요. 오직 {company}와 관련된 정보만 작성하세요.

    [분석 항목]
    - 사업 개요
    - 핵심 기술/제품
    - 경쟁력 및 시장 위치
    - 글로벌 공급망 및 고객사
    - 최근 사업 동향 (2023~2025년 기준)

    [출력 형식]
    - 회사명: {company}
    - 사업 개요: ...
    - 핵심 기술: ...
    - 경쟁력: ...
    - 공급망/고객사: ...
    - 최근 동향: ...

    --- 검색 결과 ---
    {text}
    ------------------
    """
)

# LLM 및 출력 파서 설정
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1
)
output_parser = StrOutputParser()

# 체인 구성
company_analysis_chain = company_prompt | llm | output_parser

# ✅ 분석 대상 기업 목록
company_list = [
    "삼성 SDI",
    "LG에너지솔루션",
    "동원시스템즈",
]

# ✅ 기업 분석 실행 함수
def run_company_analysis(state, top_k: int = 5):
    """
    기업 분석 에이전트 함수. Supervisor에서 호출되며, state를 통해 데이터를 전달받고 결과를 저장합니다.

    Args:
        state (dict): Supervisor에서 전달받은 상태 객체
        top_k (int): 유사도 검색에서 반환할 문서 수

    Returns:
        dict: 업데이트된 state 객체
    """
    result_dict = {}
    for company in company_list:
        try:
            logging.info(f"Analyzing: {company}")
            # 유사도 기반 문서 검색
            results = vector_db.similarity_search(company, k=top_k)
            logging.info(f"Search Results for {company}: {[r.page_content for r in results]}")
            content = "\n\n".join([r.page_content for r in results])

            # LLM에 입력
            analysis_result = company_analysis_chain.invoke({"text": content, "company": company})
            logging.info(f"LLM Output for {company}: {analysis_result}")

            # 결과 저장
            result_dict[company] = analysis_result
        except Exception as e:
            logging.error(f"Error analyzing {company}: {str(e)}")
            result_dict[company] = {"error": str(e)}

    # 결과를 state에 저장
    state["company_data"] = result_dict
    return state