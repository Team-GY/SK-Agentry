from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults

class AIAdoptionAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini", streaming=True)

        self.prompt_template = PromptTemplate.from_template(
            """다음 기업 정보를 바탕으로 AI 도입 진단 리포트를 작성해 주세요:

기업명: {company_name}
예상 투자비용: {investment_amount} 억원
AI 도입 목표: {ai_goal}

웹 검색 정보:
{web_context}

리포트는 다음 항목을 포함하세요:

# AI 도입 진단 리포트 - {company_name}

## 1. 도입 가능성 평가
(기업의 규모, 업종, 목표, 웹 정보에 따라 AI 도입 가능성 평가)

## 2. 예상 리스크
(예상되는 기술적/조직적 리스크)

## 3. 추천 전략
(성공적인 AI 도입을 위한 단계적 전략 제안)

각 항목은 3~5문장 이상 작성해 주세요.
"""
        )

    def search_web(self, company_name):
        search_tool = TavilySearchResults(k=5)
        results = search_tool.invoke({"query": f"{company_name} 기업 정보"})
        snippets = [
            f"- 제목: {res.get('title', '')}\n  내용: {res.get('content', '')}\n  URL: {res.get('url', '')}"
            for res in results
        ]
        return "\n".join(snippets)

    def run(self, input_data: dict):
        web_context = self.search_web(input_data["company_name"])

        prompt = self.prompt_template.format(
            company_name=input_data["company_name"],
            investment_amount=input_data["investment_amount"],
            ai_goal=input_data["ai_goal"],
            web_context=web_context
        )

        response = self.llm.invoke(prompt)
        return response