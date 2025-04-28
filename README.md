# 📈 AI ROI Analysis System
![ChatGPT Image 2025년 4월 28일 오후 04_41_29](https://github.com/user-attachments/assets/8cbce7e6-e51d-4a60-9f53-a6083c697788)

AI 기술 도입 시 다양한 산업군(제조, 유통, 금융 등)에서 기대할 수 있는 투자수익률(ROI)을 정량적으로 분석하고 시각화하는 Kafka 기반 Agent-Oriented 시스템입니다.

---

## 🚀 프로젝트 개요

- 사용자 입력 데이터(업종, 비용, 기대 효과)를 기반으로 투자수익률(ROI) 및 투자 회수 기간(BEP)을 계산합니다.
- Kafka 기반 비동기 Agent 통신 구조를 통해 독립적이고 확장 가능한 시스템을 구축합니다.
- Streamlit 기반 대시보드를 통해 분석 결과를 실시간으로 시각화합니다.

---

## 🧩 시스템 아키텍처
```pgsql
[User Input]
    ↓
Architect Agent
    ↓
Data Schema Agent → Research Agent
    ↓
ROI Calculator Agent ↔ Sensitivity Analysis Agent
    ↓
Visualization Agent ↔ Validator Agent
    ↓
Optimizer Agent (Optional)
    ↓
Streamlit 대시보드 출력
```
- 모든 Agent는 Kafka Topic을 통해 통신하며, Orchestrator Agent가 전체 흐름을 관리합니다.
---

## 🛠️ 주요 기술 스택

| 분류 | 기술 |
|:---|:---|
| Backend | Python (FastAPI) |
| Messaging | Apache Kafka |
| Frontend | Streamlit |
| Data Processing | pandas, numpy, scikit-learn |
| Visualization | Plotly, matplotlib |
| Infrastructure | Docker, docker-compose |

---

## 📂 프로젝트 구조

```python
ai-roi-analysis/
├── agents/
│   ├── architect_agent/
│   ├── data_schema_agent/
│   ├── research_agent/
│   ├── roi_calculator_agent/
│   ├── sensitivity_analysis_agent/
│   ├── visualization_agent/
│   ├── validator_agent/
│   └── optimizer_agent/ (Optional)
│
├── common/             # 공통 Kafka Client, Message Schema
├── configs/            # 설정 파일 (Kafka, Agent 환경설정)
├── streamlit_app/      # 사용자 대시보드
├── docker/             # Dockerfile, docker-compose.yml
├── README.md
└── .gitignore
```
---

## ⚡ 주요 기능

- **입력 데이터 스키마 검증**: 사용자 입력 유효성 체크
- **산업별 리서치 데이터 추천**: 업종 평균 절감률 제공
- **ROI 및 BEP 계산**: 투자 대비 수익 분석
- **민감도 분석**: 주요 변수 변화에 따른 ROI 시뮬레이션
- **데이터 검증**: 이상치 탐지 및 경고
- **시각화**: Streamlit을 통한 대시보드 출력
- **(옵션) 최적화 추천**: 투자 수익 극대화를 위한 전략 제안

---

## 🛠 설치 및 실행 방법

1. 저장소 클론
```bash
git clone https://github.com/your-username/ai-roi-analysis.git
cd ai-roi-analysis
```
2. Docker로 Kafka 및 Agent 컨테이너 실행

```bash
docker-compose up --build
```
3. Streamlit 대시보드 접속

```bash
cd streamlit_app
streamlit run app.py
```
기본 접속 URL: http://localhost:8501

