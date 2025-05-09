from sqlalchemy import Column, Integer, String, Text, Boolean
from api.db import Base

class Tool(Base):
    __tablename__ = "tools"

    tool_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)  # 예: "search_weekly"
    function_path = Column(String(128))                     # 예: "agents.weekly_news.search_news"
    description = Column(Text)
    is_active = Column(Boolean, default=True)