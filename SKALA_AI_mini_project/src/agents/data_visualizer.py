import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
from typing import Dict, List
import logging
import json

# 한글 폰트 설정
rc('font', family='Malgun Gothic')  # Windows 환경에서 '맑은 고딕' 사용
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

sns.set(style="whitegrid")

def visualize_forecast_separately(state):
    """
    시각화 에이전트 함수. ./output 디렉토리에서 예측 데이터를 읽어와 이미지를 생성합니다.

    Args:
        state (dict): Supervisor에서 전달받은 상태 객체

    Returns:
        dict: 업데이트된 state 객체
    """
    # 프로젝트 루트 디렉토리의 output 폴더를 참조
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output"))
    
    # output 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Output directory created at {output_dir}")

    visualization_data = {}

    # ./output 디렉토리에서 JSON 파일 읽기
    for file_name in os.listdir(output_dir):
        if file_name.endswith("_forecast.json"):  # JSON 파일만 처리
            company = file_name.replace("_forecast.json", "")  # 회사 이름 추출
            file_path = os.path.join(output_dir, file_name)

            try:
                # JSON 파일 읽기
                with open(file_path, "r", encoding="utf-8") as f:
                    forecast = json.load(f)

                # 시각화 생성
                plt.figure(figsize=(10, 6))
                plt.plot(forecast, label="Forecast")
                plt.title(f"{company} stock price forecast")
                plt.xlabel("date")
                plt.ylabel("price")
                plt.legend()

                # 이미지 저장
                image_path = os.path.join(output_dir, f"{company}_forecast.png")
                plt.savefig(image_path)
                plt.close()
                logging.info(f"Visualization saved for {company} at {image_path}")

                visualization_data[company] = {"image_path": image_path}
            except Exception as e:
                logging.error(f"Error visualizing {company}: {str(e)}")
                visualization_data[company] = {"error": str(e)}

    # 결과를 state에 저장
    state["visualization_data"] = visualization_data
    return state