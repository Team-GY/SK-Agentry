# api/auth/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, Field

from api.user.schemas.user import UserCreateResponse
from api.db import get_db
from api.user.models.user import User as UserModel
from api.auth.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    id: str = Field(..., example="skhynix")
    password: str = Field(..., example="secure1234")

@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == request.id))
    user = result.scalar_one_or_none()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 ID 또는 비밀번호입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.user_id)})

     # ✅ 사용자 정보와 함께 반환
    user_response = UserCreateResponse(
        user_id=user.user_id,
        id=user.id,
        name=user.name,
        industry=user.industry,
        scale=user.scale,
        interests=user.interests,
        budget_size=user.budget_size,
        msg="로그인 성공",
        success=True
    )

    return {"access_token": access_token, "token_type": "bearer", "user": user_response}
