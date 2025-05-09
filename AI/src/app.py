from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from api.user.routers.user import router as user_router
from api.auth.routers.auth import router as auth_router
from api.agent.routers.agent import router as agent_router
from agents import AGENT_REGISTRY, TOOL_REGISTRY
from api.init_db import init_models
from api.db import AsyncSessionLocal
from api.agent.models.agent import Agent
from api.agent.models.tool import Tool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

app = FastAPI()

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_models()
    async with AsyncSessionLocal() as session:
        await sync_registry_to_db(session)

# ✅ 입력 스키마
class CompanyInput(BaseModel):
    user_id: int
    company_name: str

class GenericInput(BaseModel):
    input_data: dict
    tools: list[str] = []

# ✅ 라우터 등록
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(agent_router)

# ✅ 에이전트 실행 엔드포인트
@app.post("/run_agent/{agent_id}")
async def run_agent(agent_id: str, input_data: GenericInput):
    base_agent = AGENT_REGISTRY.get(agent_id)
    if not base_agent:
        return {"error": f"Agent '{agent_id}' not found."}

    selected_tools = [TOOL_REGISTRY[name] for name in input_data.tools if name in TOOL_REGISTRY]

    if hasattr(base_agent, "__class__") and hasattr(base_agent.__class__, "__init__"):
        agent = base_agent.__class__(tools=selected_tools)
    else:
        agent = base_agent

    result = agent.run(input_data.input_data)
    return {"result": result}

# ✅ DB에 AGENT/TOOL 자동 등록
async def sync_registry_to_db(db: AsyncSession):
    for agent_name, agent_instance in AGENT_REGISTRY.items():
        existing = await db.execute(select(Agent).where(Agent.name == agent_name))
        if not existing.scalar_one_or_none():
            db.add(Agent(
                name=agent_name,
                display_name=agent_instance.display_name,
                description=f"{agent_name} 등록됨",
                category="기본",  # 필요 시 agent_instance로부터 추출
                llm_type="GPT-4o-mini",
                language="Python",
                features="자동 등록됨"
            ))

    for tool_name, func in TOOL_REGISTRY.items():
        # function_path 안전하게 추출
        if hasattr(func, "func") and callable(func.func):  # LangChain StructuredTool 케이스
            tool_func = func.func
            function_path = f"{tool_func.__module__}.{tool_func.__name__}"
        elif callable(func):  # 일반 함수일 경우
            function_path = f"{func.__module__}.{func.__name__}"
        else:  # 예외 fallback
            function_path = "unknown_tool_path"

        # 기존 DB에 없는 경우만 추가
        existing = await db.execute(select(Tool).where(Tool.name == tool_name))
        if not existing.scalar_one_or_none():
            db.add(Tool(
                name=tool_name,
                function_path=function_path,
                description=f"{tool_name} 툴"
            ))


    await db.commit()
