import streamlit as st
from agents.auto_chat import AutoChatbotAgent
from agents.ai_adoption import AIAdoptionAgent  # 다른 에이전트도 import

AGENTS = {
    "자동 상담 챗봇": {
        "class": AutoChatbotAgent,
        "description": "FAQ 및 고객 문의에 응답하는 자동 상담 챗봇"
    },
    "AI 도입 진단 Agent": {
        "class": AIAdoptionAgent,
        "description": "기업의 AI 도입 가능성, 리스크, 전략을 분석"
    }
}

st.session_state.setdefault("selected_agent", None)

def show_agent_list():
    st.title("🧩 AI Agent Marketplace")
    st.write("아래 에이전트 중 하나를 선택하세요:")

    for agent_name, agent_info in AGENTS.items():
        if st.button(f"🚀 {agent_name}"):
            st.session_state.selected_agent = agent_name
            st.rerun()

        st.caption(agent_info["description"])
        st.divider()

def run_agent_interface():
    agent_name = st.session_state.selected_agent
    agent_class = AGENTS[agent_name]["class"]

    st.header(f"🤖 {agent_name} 실행 중")

    if agent_name == "자동 상담 챗봇":
        if "agent_obj" not in st.session_state:
            company = st.text_input("회사명", "디자이노블")
            faq_topic = st.text_input("FAQ 주제", "배송")
            if st.button("챗봇 시작"):
                st.session_state.agent_obj = agent_class(company, faq_topic)
                st.session_state.chat_log = []
                st.rerun()

        if "agent_obj" in st.session_state:
            user_input = st.text_input("질문 입력:")
            if st.button("전송") and user_input:
                response = st.session_state.agent_obj.chat(user_input)
                result_text = response.content if hasattr(response, "content") else str(response)
                st.session_state.chat_log.append(("user", user_input))
                st.session_state.chat_log.append(("bot", result_text))
            for sender, msg in st.session_state.chat_log:
                if sender == "user":
                    st.markdown(f"🧑‍💼 **You:** {msg}")
                else:
                    st.markdown(f"🤖 **Chatbot:** {msg}")

    elif agent_name == "AI 도입 진단 Agent":
        company_name = st.text_input("회사명", "디자이노블")
        investment_amount = st.number_input("투자금액 (억원)", 100, 10000, 500)
        ai_goal = st.text_area("AI 도입 목표", "생산성 향상, 고객 분석")

        if st.button("진단 리포트 생성"):
            agent_obj = agent_class()
            input_data = {
                "company_name": company_name,
                "investment_amount": investment_amount,
                "ai_goal": ai_goal
            }
            report = agent_obj.run(input_data)
            result_text = report.content if hasattr(report, "content") else str(report)
            st.text_area("AI 도입 진단 리포트", result_text, height=400)

    if st.button("🔙 뒤로"):
        st.session_state.selected_agent = None
        if "agent_obj" in st.session_state:
            del st.session_state.agent_obj
        st.rerun()

if st.session_state.selected_agent is None:
    show_agent_list()
else:
    run_agent_interface()