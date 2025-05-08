from pydantic import BaseModel, Field, ConfigDict
from api.utils.enums import IndustryEnum, InterestEnum  

class UserBase(BaseModel):
    id: str = Field(..., example="skhynix")
    password: str = Field(..., example="secure1234")
    name: str = Field(..., example="SK 하이닉스")
    industry: IndustryEnum = Field(..., example="제조")
    scale: int = Field(..., example=1000)
    interests: InterestEnum = Field(..., example="LLM")
    budget_size: float = Field(..., example=100000000.0)

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    pass

class UserCreateResponse(UserCreate):
    user_id: int = Field(..., example=1)

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    user_id: int = Field(..., example=1)