from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import get_db
from api.user.models.user import User as UserModel
from api.user.models.user_report import UserReport
from api.user.schemas.user import UserCreate, UserCreateResponse, UserRead as UserSchema
import api.user.cruds.user as user_crud

router = APIRouter()

# 회원가입
@router.post("/register", response_model=UserSchema)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = UserModel(
        id=user_data.id,
        password=user_data.password,
        name=user_data.name,
        industry=user_data.industry,
        scale=user_data.scale,
        interests=user_data.interests,
        budget_size=user_data.budget_size,
    )

    db.add(new_user)
    await db.flush()

    for report in user_data.reports:
        new_report = UserReport(
            user_id=new_user.user_id,
            filename=report.filename,
            format=report.format,
        )
        db.add(new_report)

    await db.commit()
    await db.refresh(new_user)

    return UserSchema.model_validate(new_user)


# 전체 유저 조회
@router.get("/", response_model=list[UserSchema])
async def list_users(db: AsyncSession = Depends(get_db)):
    users = await user_crud.get_all_users(db)
    return [UserSchema.model_validate(user) for user in users]


# 특정 유저 조회
@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user


# 유저 수정
@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: str, user_update: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated = await user_crud.update_user(db, db_user, user_update)
    return UserSchema.model_validate(updated)


# 유저 삭제
@router.delete("/{user_id}")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user_crud.delete_user(db, db_user)
    return {"message": "User deleted successfully"}
