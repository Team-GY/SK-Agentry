from fastapi import FastAPI, Depends
from pydantic import BaseModel
from api.user.routers.user import router as user_router
from api.auth.routers.auth import router as auth_router
from agents import AGENT_REGISTRY
from agents import TOOL_REGISTRY
import asyncio
from api.init_db import init_models
from sqlalchemy.orm import Session
from api.user.models.user_report import UserReport
from api.db import get_db
from utils import load_vector_db
from analysis import analyze_company

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_models()

class CompanyInput(BaseModel):
    user_id: int
    company_name: str

class GenericInput(BaseModel):
    input_data: dict
    tools: list[str] = []  # 추가: tools 리스트 optional
    
# 유저 로직
app.include_router(user_router)
app.include_router(auth_router)

# 공통 agent 실행 방식
@app.post("/run_agent/{agent_id}")
async def run_agent(agent_id: str, input_data: GenericInput):
    base_agent = AGENT_REGISTRY.get(agent_id)
    if not base_agent:
        return {"error": f"Agent '{agent_id}' not found."}

    # 선택된 tools 이름 → 실제 함수로 매핑
    selected_tools = [TOOL_REGISTRY[name] for name in input_data.tools if name in TOOL_REGISTRY]

    # tools가 지원되는 agent인 경우 → 새 instance 생성 시 tools 전달
    if hasattr(base_agent, "__class__") and hasattr(base_agent.__class__, "__init__"):
        agent = base_agent.__class__(tools=selected_tools)
    else:
        agent = base_agent  # tools 지원 안 하는 agent

    result = agent.run(input_data.input_data)
    return {"result": result}

