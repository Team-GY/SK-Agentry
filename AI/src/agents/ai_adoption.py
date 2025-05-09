from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_company

class AIAdoptionAgent:
    display_name = "AI 도입 전략 추천 에이전트"
    description = (
        "기업의 규모, 산업군, 관심사 등 정보를 바탕으로 AI 도입 가능성을 진단하고 "
        "도입 전략 및 예상 효과를 리포트 형태로 제공하는 에이전트입니다. "
        "웹 및 내부 정보를 종합적으로 활용해 도입 리스크와 전략을 자동으로 제시합니다."
    )
    category = "컨설팅"
    features = "- AI 도입 가능성 평가\n- 예상 리스크 분석\n- 추천 전략 제시"

    def __init__(self, tools: list = None, temperature: float = 0.3, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(temperature=temperature, model=model, streaming=True)

        base_tools = [search_company]
        if tools:
            base_tools.extend(tools)

        self.tools = base_tools

        self.prompt_template = PromptTemplate.from_template(
            """다음 기업 정보를 바탕으로 AI 도입 진단 리포트를 작성해 주세요:

{input}

기업에 대한 정보를 수집하여 활용하세요.

리포트는 다음 항목을 포함하세요:

# AI 도입 진단 리포트

## 1. 도입 가능성 평가
## 2. 예상 리스크
## 3. 추천 전략

{agent_scratchpad}

각 항목은 3~5문장 이상 작성해 주세요.
"""
        )

        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt_template)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def run(self, input_data: dict):
        input_text = input_data.get("input")
        if not input_text:
            raise ValueError("'input' 키가 필요합니다.")
        return self.executor.invoke({"input": input_text})