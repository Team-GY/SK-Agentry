from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_news


class WeeklyNewsAgent:
    display_name = "주간 뉴스 브리핑 에이전트"
    description = (
        "지정된 주제(예: 기술, 산업, 금융 등)에 대한 최신 뉴스 콘텐츠를 수집하고 요약하여 "
        "간결한 주간 리포트 형태로 제공하는 에이전트입니다. "
        "외부 뉴스 검색 도구를 활용해 실시간 정보를 수집하고 분석합니다."
    )
    category = "정보 요약"
    features = "- 최신 뉴스 요약\n- 주간 리포트 제공\n- 실시간 정보 수집"

    def __init__(self, topic: str = "기술", tools: list = None, temperature=0, model_name="gpt-4o-mini"):
        self.topic = topic
        self.llm = ChatOpenAI(temperature=temperature, model=model_name, streaming=True)
        base_tools = [search_news]
        if tools:
            base_tools.extend(tools)
        self.tools = base_tools

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"당신은 {self.topic} 분야의 이번 주 뉴스를 요약하는 리포트 작성 전문가입니다."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])

        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def run(self, input_data: dict):
        input_text = input_data.get("input")
        if not input_text:
            raise ValueError("'input' 키가 필요합니다.")
        return self.executor.invoke({"input": input_text.replace("{topic}", self.topic)})