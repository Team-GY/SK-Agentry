from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Integer, select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from api.user.models.user import User
from api.user.schemas.user import UserCreate, UserRead
from api.utils.auth import hash_password  # 비밀번호 해시가 필요하다면
from sqlalchemy.future import select
from fastapi import HTTPException
from analysis import analyze_company

# 회원가입
async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    # 1. ID 중복 확인
    existing_user = await db.execute(select(User).where(User.id == user_data.id))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자 ID입니다.")
    
    # 2. User 생성
    new_user = User(
        id=user_data.id,
        password=hash_password(user_data.password),
        name=user_data.name,
        industry=user_data.industry,
        scale=user_data.scale,
        interests=user_data.interests,
        budget_size=user_data.budget_size
    )
    db.add(new_user)
    await db.flush()  # user_id 확보를 위해 flush

    # 4. 커밋 및 refresh
    await db.commit()
    await db.refresh(new_user)

    return new_user

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(
        select(User)
        .options(selectinload(User.reports))  
        .where(User.user_id == user_id)
    )
    return result.scalars().first()

# ✅ 유저 전체 조회 (예: 관리용)
async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(
        select(User).options(selectinload(User.reports))
    )
    return result.scalars().all()

# ✅ 유저 정보 수정
async def update_user(db: AsyncSession, original: User, update_data: UserCreate) -> User:
    original.name = update_data.name
    original.industry = update_data.industry
    original.scale = update_data.scale
    original.interests = update_data.interests
    original.budget_size = update_data.budget_size
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

# ✅ 유저 삭제
async def delete_user(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()
