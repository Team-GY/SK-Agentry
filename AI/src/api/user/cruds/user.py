from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from api.user.models.user import User
from api.user.schemas.user import UserCreate, UserCreateResponse as UserSchema
from api.utils.auth import hash_password  # 비밀번호 해시가 필요하다면

# ✅ 회원 생성
async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
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
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(new_user)
    return new_user

# ✅ 회원 ID(email)으로 조회
async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalars().first()

# ✅ 유저 전체 조회 (예: 관리용)
async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()

# ✅ 유저 정보 수정
async def update_user(db: AsyncSession, original: User, update_data: UserSchema) -> User:
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
