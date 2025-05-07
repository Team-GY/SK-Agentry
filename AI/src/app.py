from fastapi import FastAPI
from pydantic import BaseModel
from agents.ai_adoption import AIAdoptionAgent
from agents.auto_chat import AutoChatbotAgent

app = FastAPI()

# 에이전트 인스턴스
ai_adoption_agent = AIAdoptionAgent()
auto_chatbot_agent = AutoChatbotAgent()

# agent 레지스트리 등록
AGENT_REGISTRY = {
    "ai_adoption": ai_adoption_agent,
    "auto_chatbot": auto_chatbot_agent,
}

# 입력 스키마
class AIAdoptionInput(BaseModel):
    company_name: str
    investment_amount: int
    ai_goal: str

class ChatInput(BaseModel):
    user_message: str

class GenericInput(BaseModel):
    input_data: dict

# 직접 호출하는 방식
@app.post("/run-ai-adoption")
async def run_ai_adoption(input_data: AIAdoptionInput):
    result = ai_adoption_agent.run(input_data.dict())
    content = result.content if hasattr(result, "content") else str(result)
    return {"report": content}

@app.post("/run-auto-chatbot")
async def run_auto_chatbot(input_data: ChatInput):
    result = auto_chatbot_agent.chat(input_data.user_message)
    return {"response": result}

# 공통 agent 실행 방식
@app.post("/run_agent/{agent_id}")
async def run_agent(agent_id: str, input_data: GenericInput):
    agent = AGENT_REGISTRY.get(agent_id)
    if not agent:
        return {"error": f"Agent '{agent_id}' not found."}
    result = agent.run(input_data.input_data)
    return {"result": result}
