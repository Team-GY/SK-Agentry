from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, AIMessage, HumanMessage

class AutoChatbotAgent:
    display_name = "자동 대화 에이전트"
    description = (
        "기업의 자주 묻는 질문(FAQ)이나 특정 주제에 대한 상담을 자동으로 처리하는 대화형 에이전트입니다. "
        "사용자가 입력한 질문에 대해 자연스럽고 정확한 응답을 제공하며, "
        "고객센터 또는 내부 교육용 챗봇으로 활용할 수 있습니다."
    )
    category = "고객지원"
    features = "- 자주 묻는 질문 자동 응답\n- 고객 상담 지원\n- 내부 교육 자료 제공"

    def __init__(self, company_name: str = "기본회사", faq_topic: str = "자주 묻는 질문"):
        self.company_name = company_name
        self.faq_topic = faq_topic
        self.llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini", streaming=True)

        self.chat_history = [
            SystemMessage(content=f"당신은 {self.company_name}의 {self.faq_topic}에 대한 자동 상담 챗봇입니다. 사용자 질문에 친절하고 명확하게 답하세요.")
        ]

    def chat(self, user_input: str):
        self.chat_history.append(HumanMessage(content=user_input))
        response = self.llm.invoke(self.chat_history)
        self.chat_history.append(AIMessage(content=response.content))
        return response.content

    def run(self, input_data: dict):
        user_input = input_data.get("input")
        if not user_input:
            raise ValueError("'input' key가 필요합니다.")
        return self.chat(user_input)