from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

summary_prompt_template = PromptTemplate.from_template(
    """
당신은 기업 디지털 전환 분석 전문가입니다.

다음은 [{company_name}]에 대한 외부 웹 검색 결과와 내부 문서 분석 내용입니다.

[🔍 웹 검색 정보]
{web_context}

[📄 내부 문서 요약]
{pdf_context}

이 기업은 아래와 같은 **정확한 사용자 입력 정보**를 바탕으로 분석되어야 합니다:  
- 산업군: {industry}  
- 직원 수(기업 규모): {scale}명  
- 주요 관심사: {interests}  
- 예산 규모: {budget_size:,}원  
- 리포트 생성일: {created_date}  

⚠️ 위 수치들은 사용자 데이터베이스에 저장된 실제 값이므로, 분석 결과에 **그대로 반영**되어야 하며, **LLM이 임의로 다른 숫자를 생성하지 마십시오**.

이제 위 정보를 기반으로 다음과 같은 형식의 **AI 도입 리포트 (Markdown)** 를 작성해 주세요.

---

# 📊 {company_name} AI 에이전트 도입 리포트

> 발행일: {created_date}  
> 분석 대상: {company_name}  
> 산업군: {industry}  
> 기업 규모: {scale}
> 기술 도입 경험: 내부 문서와 검색 결과에 기반해 요약

---

## 🧭 1. 디지털 성숙도 분석

- 기술 도입 단계 (1~5단계 중 하나, 예: 도입 초기/중간/선진)
- 이미 보유한 기술 (bullet point 나열)
- 경쟁사 대비 강점/약점 요약

---

## 🤖 2. 추천 AI 에이전트

| 에이전트명 | 적용 부서 | 적용 사례 | 연간 절감 시간 | 도입 난이도 |
|------------|------------|------------|----------------|--------------|
| 예시: 고객 피드백 분석 AI | 마케팅팀 | 고객 리뷰 분석 | 1,200시간 | 낮음 |
| 예시: 업무 자동화 Agent | 인사팀 | 반복 업무 자동화 | 1,000시간 | 중 |

---

## 💹 3. 도입 효과 분석 (ROI)

- 예산 규모: {budget_size:,}원  
- 절감 시간 예측: 내부 데이터 기반으로 유추  
- 인건비 환산 예시: 시간당 30,000원 가정  
- ROI 계산 예시: (절감액 ÷ {budget_size:,}원) × 100%  
- ⚠️ 예산은 위 입력값을 기준으로 계산하십시오. 임의 수치를 생성하지 마십시오.

---

## ⚠️ 4. 리스크 및 고려사항

- 정확도, 보안성, 직원 수용성
- 기술 인프라 요구사항
- 도입 이후 운영 및 유지보수 계획

---

## 🚀 5. 다음 단계 제안

1. AI 에이전트 PoC 테스트
2. 우선 적용 부서 선정
3. 정식 도입 전 직원 교육 및 반응 조사

---

## ✅ 6. 요약 (Executive Summary)

- {company_name}의 AI 도입 가능성 및 기대 효과 요약
- 특히 유효한 적용 영역 2~3개
- 예산 대비 ROI 요약 (정량 지표 사용)

---

**📬 담당자 문의**: ai-support@sk-agentry.ai  
**🧠 Powered by**: SK Agentry AI Market
"""
)


summary_prompt = summary_prompt_template

llm = ChatOpenAI(temperature=0, model='gpt-4o-mini', streaming=True)

summary_chain = LLMChain(llm=llm, prompt=summary_prompt)