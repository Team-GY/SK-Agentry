from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from datetime import datetime

today_str = datetime.today().strftime("%Y년 %m월 %d일")

load_dotenv()

# LLM
llm = ChatOpenAI(temperature=0, model='gpt-4o-mini', streaming=True)

# JSON Output Parser
recommend_parser = JsonOutputParser()

# --- Recommend Prompt
recommend_prompt_template = PromptTemplate.from_template(
    """아래는 [{company_name}]에 대한 웹 검색 정보와 내부 문서 검색 결과입니다.

[웹 검색 정보]
{web_context}

[내부 문서 검색]
{pdf_context}

위 정보를 바탕으로 이 기업에 가장 유용할 AI Agent를 3가지 추천해 주세요.

{format_instructions}
"""
)
recommend_prompt = recommend_prompt_template.partial(
    format_instructions=recommend_parser.get_format_instructions()
)
recommend_chain = LLMChain(llm=llm, prompt=recommend_prompt, output_parser=recommend_parser)

# --- Summary Prompt
from langchain.prompts import PromptTemplate

summary_prompt_template = PromptTemplate.from_template(
    """
당신은 기업 디지털 전환 분석 전문가입니다.

다음은 [{company_name}]에 대한 외부 웹 검색 결과와 내부 문서 분석 내용입니다.

[🔍 웹 검색 정보]
{web_context}

[📄 내부 문서 요약]
{pdf_context}

이 정보를 바탕으로 **아래 형식의 Markdown 리포트**를 생성해주세요.  
해당 기업이 AI 에이전트를 도입할 수 있는 영역을 식별하고, 도입 효과를 정량적으로 예측하며,  
경영진이 설득될 수 있도록 실제 수치와 인사이트를 포함합니다.

---

# 📊 {company_name} AI 에이전트 도입 리포트

> 발행일: {today_str}  
> 분석 대상: {company_name}  
> 산업군: 분석 내용을 기반으로 판단 (예: 제조, 유통, 금융 등)  
> 기업 규모: (직원 수 기준 – 스타트업, 중소기업, 대기업 등)  
> 기술 도입 경험: 이전 도입 기술 또는 관련 활동 요약

---

## 🧭 1. 디지털 성숙도 분석

- 기술 도입 단계 (1~5단계 중 하나, 예: 도입 초기/중간/선진)
- 이미 보유한 기술 (bullet point 나열)
- 경쟁사 대비 강점/약점 요약

---

## 🤖 2. 추천 AI 에이전트

| 에이전트명 | 적용 부서 | 적용 사례 | 연간 절감 시간 | 도입 난이도 |
|------------|------------|------------|----------------|--------------|
| 예시: 회의 요약 Agent | 기획팀 | 회의 기록 자동 정리 | 1,200시간 | 중 |
| 예시: 고객 문의 응대 Agent | 고객지원팀 | 챗봇 응대 자동화 | 2,000시간 | 낮음 |

---

## 💹 3. 도입 효과 분석 (ROI)

- 연간 총 절감 시간 × 인건비 환산 (금액 표기)
- 예상 도입/운영 비용
- ROI 계산 (절감 비용 ÷ 도입 비용 × 100%)
- 주의사항 또는 적용 조건

---

## ⚠️ 4. 리스크 및 고려사항

- 정확도, 보안성, 직원 수용성
- 기술 인프라 요구사항
- 도입 이후 관리 이슈

---

## 🚀 5. 다음 단계 제안

1. AI 에이전트 시뮬레이션 테스트
2. 내부 우선 적용 대상 부서 지정
3. PoC 또는 베타 적용 제안

---

## ✅ 6. 요약 (Executive Summary)

- 해당 기업의 디지털 인프라 및 AI 활용 가능성에 대한 평가
- 도입이 특히 유효한 영역 (2~3가지)
- 연간 절감 효과 예상치 및 ROI 개략치

---

**📬 담당자 문의**: ai-support@sk-agentry.ai  
**🧠 Powered by**: SK Agentry AI Market
"""
)

summary_prompt = summary_prompt_template.partial(today_str=today_str)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)