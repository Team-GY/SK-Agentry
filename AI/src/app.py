from fastapi import FastAPI, Depends
from pydantic import BaseModel
from api.user.routers.user import router as user_router
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
app.include_router(user_router, prefix="/auth")

# # 기업 분석 실행 API
# @app.post("/analyze")
# def analyze(input_data: CompanyInput, db_session: Session = Depends(get_db)):
#     vector_db = load_vector_db()
#     result = analyze_company(input_data.company_name, vector_db)

#     report = UserReport(
#         user_id=input_data.user_id,  # CompanyInput 모델에 user_id 추가 필요
#         filename=result["summary_report_file"],
#         format="md"
#     )
#     db_session.add(report)
#     db_session.commit()

#     return {
#         "report_id": report.user_report_id,
#         "filename": report.filename,
#         "format": report.format
#     }
# 공통 agent 실행 방식
@app.post("/run_agent/{agent_id}")
async def run_agent(agent_id: str, input_data: GenericInput):
    agent = AGENT_REGISTRY.get(agent_id)
    if not agent:
        return {"error": f"Agent '{agent_id}' not found."}
    result = agent.run(input_data.input_data)
    return {"result": result}


