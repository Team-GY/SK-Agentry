from fastapi import FastAPI, Depends
from pydantic import BaseModel
from api.user.routers.user import router as user_router
from api.auth.routers.auth import router as auth_router
from agents import AGENT_REGISTRY
import asyncio
from api.init_db import init_models

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_models()

class CompanyInput(BaseModel):
    user_id: int
    company_name: str

class GenericInput(BaseModel):
    input_data: dict

# 유저 로직
app.include_router(user_router)
app.include_router(auth_router)

# 공통 agent 실행 방식
@app.post("/run_agent/{agent_id}")
async def run_agent(agent_id: str, input_data: GenericInput):
    agent = AGENT_REGISTRY.get(agent_id)
    if not agent:
        return {"error": f"Agent '{agent_id}' not found."}
    result = agent.run(input_data.input_data)
    return {"result": result}


