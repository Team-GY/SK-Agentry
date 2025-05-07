from fastapi import FastAPI
from pydantic import BaseModel
from agents.ai_adoption import AIAdoptionAgent
from agents.auto_chat import AutoChatbotAgent

app = FastAPI()

ai_adoption_agent = AIAdoptionAgent()
auto_chatbot_agent = AutoChatbotAgent()

class AIAdoptionInput(BaseModel):
    company_name: str
    investment_amount: int
    ai_goal: str

class ChatInput(BaseModel):
    user_message: str

@app.post("/run-ai-adoption")
async def run_ai_adoption(input_data: AIAdoptionInput):
    result = ai_adoption_agent.run(input_data.dict())
    content = result.content if hasattr(result, "content") else str(result)
    return {"report": content}

@app.post("/run-auto-chatbot")
async def run_auto_chatbot(input_data: ChatInput):
    result = auto_chatbot_agent.chat(input_data.user_message)
    return {"response": result}