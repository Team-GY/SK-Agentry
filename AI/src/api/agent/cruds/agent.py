from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import os
from fastapi import HTTPException

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