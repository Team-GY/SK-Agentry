from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_news


class WeeklyNewsAgent:
    display_name = "주간 뉴스 브리핑 에이전트"
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