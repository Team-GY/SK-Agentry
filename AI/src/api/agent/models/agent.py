from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from api.db import Base

class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)       # 에이전트 ID (예: "ai_adoption")
    display_name = Column(String(128), nullable=False)           # 사용자에게 보여지는 이름
    description = Column(Text)                                   # 에이전트 설명
    category = Column(String(64))                                # 분류 (예: "LLM", "자동화")
    llm_type = Column(String(64))                                # 사용 모델 (예: "GPT-4", "SLLM")
    language = Column(String(32))                                # 언어 (예: "Python")
    features = Column(Text)                                      # 주요 기능 (Markdown 혹은 JSON 문자열)
    is_active = Column(Boolean, default=True)                    # 활성화 여부
    image_url = Column(String(256), nullable=True)               # 이미지 URL

    recommended_agents = relationship("RecommendedAgent", back_populates="agent")