from typing import List
from pydantic import BaseModel, Field, ConfigDict
from api.user.schemas.user_report import UserCreateReport, UserReportResponse
from api.utils.enums import IndustryEnum, InterestEnum  

# 📌 공통 필드 정의 (password는 제외)
class UserBase(BaseModel):
    id: str = Field(..., example="skhynix")
    name: str = Field(..., example="SK 하이닉스")
    industry: IndustryEnum = Field(..., example="제조")
    scale: int = Field(..., example=1000)
    interests: InterestEnum = Field(..., example="LLM")
    budget_size: float = Field(..., example=100000000.0)
    reports: List[UserReportResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

# 📌 회원 생성 요청 시 사용 (password 포함)
class UserCreate(UserBase):
    password: str = Field(..., example="secure1234")

# 📌 회원 조회 응답용 (password 제외)
class UserCreateResponse(UserBase):
    user_id: int = Field(..., example=1)
    msg: str = Field(..., example="사용자가 성공적으로 생성되었습니다.")

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)