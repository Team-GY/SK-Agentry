from pydantic import BaseModel, Field, ConfigDict
from api.utils.enums import ReportTypeEnum

class UserReportBase(BaseModel):
    user_id: int = Field(..., example=1)
    filename: str = Field(..., example="삼성전자_report.md")
    format: ReportTypeEnum = Field(..., example="MD")

    model_config = ConfigDict(from_attributes=True)

class UserCreateReport(UserReportBase):
    pass

class UserReportResponse(UserReportBase):
    user_report_id: int = Field(..., example=1)