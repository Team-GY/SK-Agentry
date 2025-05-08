from fastapi import FastAPI
from pydantic import BaseModel
from agents.ai_adoption import AIAdoptionAgent
from agents.auto_chat import AutoChatbotAgent
from analysis import analyze_company
from utils import load_vector_db


app = FastAPI()

ai_adoption_agent = AIAdoptionAgent()
auto_chatbot_agent = AutoChatbotAgent()

class CompanyInput(BaseModel):
    company_name: str

class AIAdoptionInput(BaseModel):
    company_name: str
    investment_amount: int
    ai_goal: str

class ChatInput(BaseModel):
    user_message: str

app = FastAPI()

db = load_vector_db()

# 플랫폼 Agent
## 기업 분석 에이전트 API
@app.post("/run-analyze")
def analyze(input_data: CompanyInput):
    result = analyze_company(input_data.company_name, db)
    return {
        # "recommended_agents": result["recommended_agents"],
        "report_file": result["summary_report_file"]
    }



# 판매용 Agent
## ai 도입 진단 agent
@app.post("agent/ai-adoption")
async def run_ai_adoption(input_data: AIAdoptionInput):
    result = ai_adoption_agent.run(input_data.dict())
    content = result.content if hasattr(result, "content") else str(result)
    return {"report": content}

## 자동 챗봇 agent
@app.post("agent/auto-chat")
async def run_auto_chatbot(input_data: ChatInput):
    result = auto_chatbot_agent.chat(input_data.user_message)
    return {"response": result}