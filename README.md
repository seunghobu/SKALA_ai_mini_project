# 배터리 산업 동향 보고서 작성 에이전트 구축

본 프로젝트는 배터리 시장 트렌트를 분석하는 멀티 에이전트를 설계하고 구현하는 실습 프로젝트입니다.

## Overview

- Objective : 구갠 배터리 업계의 사업 현황 분석 및 주식 리포트 생성
- Methods : Multi-Agent, RAG, LLM 기반 보고서 생성 
- Tools : LangGraph, LangChain, OpenAI GPT API
## Features

-  배터리 산업 트렌드 분석을 위한 시장 정보 자동 수집 및 요약
- 주요 기업별 사업 전략 및 주가 흐름 자동 분석
- 수집한 주가 데이터 기반 주가 예측 시계열 차트 생성 및 종합 리포트 작성


## Tech Stack 

| Category   | Details                      |
|------------|------------------------------|
| Framework  | LangGraph, LangChain, Python |
| LLM        | GPT-4o-mini via OpenAI API   |
| Retrieval  |  Chroma DB               |


## 프로젝트 에이전트 역할 및 업무 내용

### Market_Researcher
- 배터리 산업 시장 동향 분석 (전기차 수요 증가, 북미 시장 상황)
- IRA(인플레이션 감축법)의 영향 평가
- 배터리 소재 및 공급망 동향 분석
- 배터리 제조 관련 최신 기술 트렌드 조사
- 미국의 관세 정책이 배터리 시장에 미치는 영향 분석

### Company_Analyzer
- 삼성 SDI, LG에너지솔루션, 동원시스템즈 3개 기업 분석
- 각 기업의 사업 개요 및 사업 전략 분석
- 각 기업의 핵심 기술 및 제품 라인업 평가
- 각 기업의 경쟁력 및 시장 위치 분석
- 기업별 글로벌 공급망 및 주요 고객사 파악
- 2023~2025년 기준 각 기업의 최근 사업 동향 분석

### Stock_Price_Predictor
- 3개 기업(삼성 SDI, LG에너지솔루션, 동원시스템즈)의 향후 1~3개월 주가 예측
- Transformer 모델을 활용한 주가 예측 분석
- 각 기업별 주가 상승/하락 트렌드 판단
- 예측 결과에 대한 근거 제시 및 해석

### Data_Visualizer
- 각 기업별 주가 예측 그래프 생성
- 시각적 데이터 표현을 통한 주가 트렌드 시각화
- 주가 예측 결과의 효과적인 시각화 구현

### Report_Generator
- 기업 분석, 시장 분석, 주가 예측, 시각화 결과를 종합한 통합 보고서 작성
- 보고서의 구조화 및 포맷팅 (서론, 기업 분석, 시장 분석, 주가 예측, 시각화)
- 다양한 포맷(HTML, MD, PDF, TXT)의 보고서 생성

### Supervisor
- 전체 워크플로우 관리 및 조정
- 각 에이전트 간 데이터 흐름 제어
- 단계별 작업 완료 확인 및 다음 단계 진행 지시
- 각 에이전트의 결과물 통합 및 최종 보고서 생성 감독
- 에러 처리 및 로깅


## State 
- init : 프로젝트의 시작 지점. Supervisor가 전체 흐름과 각 Agent의 실행 순서 결정
- market_research : EV 산업의 시장 동향, 부품 공급망, 기술 트렌드 수집 및 요약
- company_analysis : 주요 완성차 기업의 전기차 관련 전략, 제품 강점 등을 분석
- stock_price_analysis : 주가 데이터를 수집하고 시계열 예측으로 주가 흐름 분석
- data_visualization : 주가 및 정량 데이터 기반 시각화
- report_compilation : 개별 분석 결과들을 종합해 최종 전기차 산업 보고서 작성
- end : 리포트 생성이 완료되고 최종 결과 반환

## 디렉토리 구성 
```
SKALA_AI_MINI_PROJECT/
├── .env                       # 환경 변수 설정 파일
├── Agent_Graph.png            # 에이전트 워크플로우 그래프 이미지
├── README.md                  # 프로젝트 설명 문서
├── requirements.txt           # 필요한 패키지 목록
├── output/                    # 중간 출력 결과 저장
├── pdfs/                      # PDF 형식 데이터
├── raw/                       # 원시 데이터 파일들
├── results/                   # 결과 저장 디렉토리
│   └── final_reports/         # 최종 보고서 저장 폴더
│       ├── Battery_Industry_Report.html  # HTML 형식 보고서
│       ├── Battery_Industry_Report.md    # 마크다운 형식 보고서
│       ├── Battery_Industry_Report.pdf   # PDF 형식 보고서
│       └── Battery_Industry_Report.txt   # 텍스트 형식 보고서
├── src/                       # 소스 코드
│   ├── __pycache__/           # 파이썬 캐시 파일
│   ├── agents/                # 에이전트 모듈
│   │   ├── __pycache__/       # 파이썬 캐시 파일
│   │   ├── __init__.py        # 패키지 초기화 파일
│   │   ├── company_analysis.py# 기업 분석 에이전트
│   │   ├── data_visualizer.py # 데이터 시각화 에이전트
│   │   ├── market_analysis.py # 시장 분석 에이전트
│   │   ├── report_generator.py# 보고서 생성 에이전트
│   │   ├── stock_price_predictor.py # 주가 예측 에이전트
│   │   └── supervisor.py      # 전체 에이전트 오케스트레이션
│   ├── fetcher/               # 데이터 수집 모듈
│   │   ├── __pycache__/       # 파이썬 캐시 파일
│   │   ├── __init__.py        # 패키지 초기화 파일
│   │   └── stock_data_fetcher.py # 주식 데이터 수집기
│   └── models/                # 모델 정의 모듈
│       ├── __pycache__/       # 파이썬 캐시 파일
│       ├── __init__.py        # 패키지 초기화 파일
│       └── stock_predictor_model.py # 주가 예측 모델
├── vectorstores/              # 벡터 저장소
│   ├── battery_db/            # 배터리 산업 관련 벡터 데이터베이스
│   └── company_db/            # 기업 정보 벡터 데이터베이스

```

## Setup & Installation

1. 환경 설정

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```


2. API 설정

```bash
# .env 파일에 필요한 API 키 입력
```

3. 실행

```bash
supervisor.py
```

