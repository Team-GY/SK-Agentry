from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import get_db
from api.user.schemas.user import UserCreate, UserCreateResponse, User
import api.user.cruds.user as user_crud

router = APIRouter()

# 회원가입
@router.post("/register", response_model=UserCreateResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await user_crud.create_user(db, user)
    return new_user

# 전체 유저 조회
@router.get("/", response_model=list[User])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await user_crud.get_all_users(db)

# 특정 유저 조회
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 유저 수정
@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: User, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_crud.update_user(db, db_user, user_update)

# 유저 삭제
@router.delete("/{user_id}")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    db_user = await user_crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user_crud.delete_user(db, db_user)
    return {"message": "User deleted successfully"}
