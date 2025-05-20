import sys
import os
import logging

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 에이전트 함수 임포트
from src.agents.company_analysis import run_company_analysis
from src.agents.market_analysis import run_battery_market_agent
from src.agents.stock_price_predictor import predict_stock_prices
from src.agents.data_visualizer import visualize_forecast_separately
from src.agents.report_generator import generate_report

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 1. State 정의
class State(TypedDict):
    company_data: dict
    market_data: dict
    stock_data: dict
    visualization_data: dict
    report: dict

# 2. StateGraph 생성
graph_builder = StateGraph(State)

# 3. 노드 추가
graph_builder.add_node("market_research", run_battery_market_agent)
graph_builder.add_node("company_analysis", run_company_analysis)
graph_builder.add_node("stock_price_analysis", predict_stock_prices)
graph_builder.add_node("data_visualization", visualize_forecast_separately)
graph_builder.add_node("report_generation", generate_report)

# 4. 엣지 추가 (흐름 정의)
graph_builder.add_edge(START, "market_research")
graph_builder.add_edge("market_research", "company_analysis")
graph_builder.add_edge("company_analysis", "stock_price_analysis")
graph_builder.add_edge("stock_price_analysis", "data_visualization")
graph_builder.add_edge("data_visualization", "report_generation")
graph_builder.add_edge("report_generation", END)

# 5. 그래프 컴파일
graph = graph_builder.compile()

# 6. Supervisor 실행
if __name__ == "__main__":
    print("Supervisor 실행 시작")

    # 초기 상태 정의
    initial_state = {
        "company_data": None,         # 기업 분석 결과
        "market_data": None,          # 시장 분석 결과
        "stock_data": None,           # 주가 예측 결과
        "visualization_data": None,   # 시각화 데이터
        "report": None                # 최종 보고서
    }

    print(f"초기 상태: {initial_state}")  # 디버깅 메시지 추가

    try:
        # 그래프 실행
        result = graph.invoke(initial_state)

        # 실행 결과 출력
        print("Supervisor 실행 완료")
        print("Stock Data:", result.get("stock_data", {}))  # 주가 예측 결과 디버깅
        print("Visualization Data:", result.get("visualization_data", {}))  # 시각화 결과 디버깅
        print("최종 보고서 경로:", result.get("report", {}).get("file_path", "보고서 생성 실패"))
        print("최종 보고서 요약:")
        print(result.get("report", {}).get("summary", "요약 없음"))
    except Exception as e:
        logging.error(f"Supervisor 실행 중 오류 발생: {e}")
        print(f"Supervisor 실행 중 오류 발생: {e}")