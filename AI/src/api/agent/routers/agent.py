from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
from api.auth.auth import get_current_user
from api.user.models.user import User as UserModel
from api.user.models.user_report import UserReport
from api.user.schemas.user_report import UserCreateReport, UserReportResponse
from api.utils.enums import ReportTypeEnum
from api.agent.cruds import agent as report_crud

from analysis import analyze_company  # 분석 로직 및 벡터 DB 로더
from pydantic import BaseModel
from tools import load_vector_db  # 벡터 DB 로더

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/analyze", response_model=UserReportResponse)
async def run_company_analysis(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # ✅ 회사명은 로그인된 유저의 이름으로 자동 설정
    company_name = current_user.name

    # ✅ 유저 기반 분석 메타 정보 구성
    user_data = {
        "industry": current_user.industry.value if current_user.industry else "정보 없음",
        "scale": "스타트업" if current_user.scale < 50 else "중소기업" if current_user.scale < 300 else "대기업",
        "interests": current_user.interests.value if current_user.interests else "정보 없음",
        "budget_size": current_user.budget_size,
        "created_date": current_user.created_date,
    }

    # 1. 벡터 DB 불러오기
    vector_db = load_vector_db()

    # 2. 분석 실행
    result = analyze_company(company_name, vector_db, user_data)

    # 3. 리포트 저장
    report_data = UserCreateReport(
        user_id=current_user.user_id,
        filename=result["summary_report_file"],
        format=ReportTypeEnum.MD
    )
    new_report = await report_crud.create_user_report(db, report_data)

    return new_report



# ✅ 리포트 전체 조회 (현재 로그인 유저 기준)
@router.get("/", response_model=list[UserReportResponse])
async def get_my_reports(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    reports = await report_crud.get_reports_by_user_id(db, current_user.user_id)
    return reports


# ✅ 단일 리포트 조회
@router.get("/{report_id}", response_model=UserReportResponse)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    report = await report_crud.get_report_by_id(db, report_id)
    if report is None or report.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")
    return report


@router.get("/report/{report_id}/content", response_model=str)
async def get_report_content(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # 1. 리포트 조회
    report = await report_crud.get_report_by_id(db, report_id)
    if report is None or report.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")

    # 2. 파일 읽기 (CRUD 함수 활용)
    content = await report_crud.read_report_markdown_content(report)
    return content