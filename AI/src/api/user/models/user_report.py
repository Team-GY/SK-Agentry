from sqlalchemy import Column, Enum, ForeignKey, Integer, DateTime, Text
from datetime import datetime

from AI.src.api.db import Base

class UserReport(Base):
    __tablename__ = "user_reports"
    user_report_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    filename = Column(Text, nullable=False)
    format = Column(Enum("md", "pdf", "html", name="report_format_enum"))
    created_date = Column(DateTime, default=datetime.utcnow)
    modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)