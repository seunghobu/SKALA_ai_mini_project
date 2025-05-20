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


## Agents
 
- Market_Researcher : EV 시장조사, KD 및 부품 공급 동향 조사, 기술 트렌드 조사
- Company_Analyzer : 자동차 기업별 전기차 사업 전략 및 제품 분석
- Stock_Price_Predictor :주가 분석 및 예측(Transformer  적용)
- Data Visualization : 주가 변화 차트 생성
- Report Generator : 최종 리포트 통합
- Supervisor : 흐름 제어, 에이전트 역할 판단


## State 
- init : 프로젝트의 시작 지점. Supervisor가 전체 흐름과 각 Agent의 실행 순서 결정
- market_research : EV 산업의 시장 동향, 부품 공급망, 기술 트렌드 수집 및 요약
- company_analysis : 주요 완성차 기업의 전기차 관련 전략, 제품 강점 등을 분석
- stock_price_analysis : 주가 데이터를 수집하고 시계열 예측으로 주가 흐름 분석
- data_visualization : 주가 및 정량 데이터 기반 시각화
- report_compilation : 개별 분석 결과들을 종합해 최종 전기차 산업 보고서 작성
- end : 리포트 생성이 완료되고 최종 결과 반환

## Architecture
![모델구조](C:\Users\Administrator\Desktop\SKALA_AI_mini_project\Agent_Graph.png)
