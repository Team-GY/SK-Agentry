from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

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
summary_prompt_template = PromptTemplate.from_template(
    """아래 정보를 기반으로 리포트를 작성해 주세요:

웹 검색 정보:
{web_context}

문서 검색:
{pdf_context}

리포트는 마크다운 형식이며 아래 항목을 포함합니다:

# {company_name} 기업 분석 리포트

## 1. 기업 개요
- 간단 설명
- 연혁 요약
- 마크다운 표: 설립년도, 직원 수, 매출, 본사 위치

## 2. 주요 사업
- 각 사업 부문 설명
- 마크다운 표: 사업명, 매출 비율, 주요 제품

## 3. 경영·사업 동향
- 최근 경영 전략
- 신규 사업 추진 현황
- 조직 개편, 리더십 변화
- 시장/경쟁 동향 대응
- bullet point로 최근 주요 이슈 정리

## 4. 비즈니스 인사이트
- 분석가 관점 요약
- bullet point
"""
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt_template)