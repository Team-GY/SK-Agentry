from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, AIMessage, HumanMessage

class AutoChatbotAgent:
    def __init__(self, company_name: str = "기본회사", faq_topic: str = "자주 묻는 질문"):
        self.company_name = company_name
        self.faq_topic = faq_topic
        self.llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini", streaming=True)

        # system message로 프롬프트 초기화
        self.chat_history = [
            SystemMessage(content=f"당신은 {self.company_name}의 {self.faq_topic}에 대한 자동 상담 챗봇입니다. 사용자 질문에 친절하고 명확하게 답하세요.")
        ]

    def chat(self, user_input: str):
        # 사용자 메시지 추가
        self.chat_history.append(HumanMessage(content=user_input))

        # LLM 응답
        response = self.llm.invoke(self.chat_history)

        # 응답 메시지 저장
        self.chat_history.append(AIMessage(content=response.content))

        return response.content