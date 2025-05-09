from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.db import Base

class RecommendedAgent(Base):
    __tablename__ = "recommended_agents"

    recommended_agent_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.agent_id"), nullable=False)

    user = relationship("User", back_populates="recommended_agents")
    agent = relationship("Agent")