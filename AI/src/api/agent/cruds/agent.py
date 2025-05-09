from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from api.agent.models.recommended import RecommendedAgent
from api.agent.models.agent import Agent
from api.user.models.user_report import UserReport
from api.user.schemas.user_report import UserCreateReport


# ✅ 리포트 생성
async def create_user_report(db: AsyncSession, report_data: UserCreateReport) -> UserReport:
    new_report = UserReport(
        user_id=report_data.user_id,
        filename=report_data.filename,
        format=report_data.format
    )
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    return new_report

# ✅ 추천 에이전트 저장
async def create_recommended_agents(
    db: AsyncSession,
    user_id: int,
    recommended_agents: list[dict]
):
    saved_records = []

    for agent_info in recommended_agents:
        agent_name = agent_info.get("에이전트명")

        # Agent 테이블에서 agent_id 찾기
        result = await db.execute(select(Agent).where(Agent.name == agent_name))
        agent_record = result.scalars().first()

        if not agent_record:
            # 없는 경우 → 스킵하거나 로그 처리
            print(f"⚠️ Agent '{agent_name}' not found in Agent table.")
            continue

        # 추천 에이전트 레코드 생성
        new_rec_agent = RecommendedAgent(
            user_id=user_id,
            agent_id=agent_record.agent_id
        )
        db.add(new_rec_agent)
        saved_records.append(new_rec_agent)

    await db.commit()
    return saved_records


# ✅ 유저별 리포트 전체 조회
async def get_reports_by_user_id(db: AsyncSession, user_id: int) -> list[UserReport]:
    result = await db.execute(
        select(UserReport).where(UserReport.user_id == user_id)
    )
    return result.scalars().all()


# ✅ 단일 리포트 조회
async def get_report_by_id(db: AsyncSession, report_id: int) -> UserReport | None:
    result = await db.execute(
        select(UserReport).where(UserReport.user_report_id == report_id)
    )
    return result.scalar_one_or_none()


async def read_report_markdown_content(report: UserReport) -> str:
    if not os.path.isfile(report.filename):
        raise HTTPException(status_code=404, detail="Markdown 파일이 존재하지 않습니다.")

    try:
        with open(report.filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 읽기 오류: {str(e)}")
    
# ✅ 추천 에이전트 가져오기
async def get_recommended_agents_by_user(
    db: AsyncSession, user_id: int
) -> list[dict]:
    result = await db.execute(
        select(RecommendedAgent)
        .options(selectinload(RecommendedAgent.agent))
        .where(RecommendedAgent.user_id == user_id)
    )
    records = result.scalars().all()
    return [
        {
            "user_id": rec.user_id,
            "agent_id": rec.agent.agent_id,
            "agent_name": rec.agent.name,
            "display_name": rec.agent.display_name,
            "category": rec.agent.category,
            "llm_type" : rec.agent.llm_type,
        }
        for rec in records
    ]

# ✅ 단일 에이전트 상세 조회
async def get_agent_by_id(db: AsyncSession, agent_id: int) -> dict | None:
    result = await db.execute(
        select(Agent).where(Agent.agent_id == agent_id)
    )
    agent = result.scalar_one_or_none()

    if not agent:
        return None

    return {
        "agent_id": agent.agent_id,
        "name": agent.name,
        "display_name": agent.display_name,
        "description": agent.description,
        "category": agent.category,
        "llm_type": agent.llm_type,
        "language": agent.language,
        "features": agent.features,
        "is_active": agent.is_active,
        "image_url": agent.image_url,
    }