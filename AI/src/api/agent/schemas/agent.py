from pydantic import BaseModel, Field
from typing import Optional

class AgentBase(BaseModel):
    name: str = Field(..., example="ai_adoption")
    display_name: str = Field(..., example="AI 도입 추천 에이전트")
    description: Optional[str] = Field(None, example="AI 도입 우선순위를 평가하고 ROI를 분석합니다.")
    category: Optional[str] = Field(None, example="LLM")
    llm_type: Optional[str] = Field(None, example="GPT-4")
    language: Optional[str] = Field(None, example="Python")
    features: Optional[str] = Field(None, example="- 고객 분석\n- 자동화 추천")
    image_url: Optional[str] = Field(None, example="/images/ai_adoption.png")

class AgentCreate(AgentBase):
    pass

class AgentResponse(BaseModel):
    agent_id: int
    name: str
    display_name: str
    description: Optional[str]
    category: Optional[str]
    llm_type: Optional[str]
    language: Optional[str]
    features: Optional[str]
    is_active: bool
    image_url: Optional[str]

    class Config:
        orm_mode = True