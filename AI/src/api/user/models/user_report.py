from sqlalchemy import Column, Enum, ForeignKey, Integer, DateTime, Text
from datetime import datetime
from sqlalchemy.orm import relationship
from api.utils.enums import ReportTypeEnum

from api.db import Base

class UserReport(Base):
    __tablename__ = "user_reports"

    user_report_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    filename = Column(Text, nullable=False)
    format = Column(Enum(ReportTypeEnum), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="reports")