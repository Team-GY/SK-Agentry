from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import get_db
from api.auth.auth import get_current_user
from api.user.models.user import User as UserModel
from api.user.schemas.user import UserCreate, UserCreateResponse, UserRead as UserSchema
import api.user.cruds.user as user_crud

router = APIRouter(prefix="/user", tags=["User"])


# ✅ 회원가입은 인증 불필요
@router.post("/register", response_model=UserCreateResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await user_crud.create_user(db, user_data)
    return UserCreateResponse.model_validate(
        {
            **new_user.__dict__,
            "msg": "사용자가 성공적으로 생성되었습니다.",
        },
        from_attributes=True,
    )


# ✅ 모든 유저 조회 (관리자 API라면 인증 + 권한 체크 필요)
@router.get("/", response_model=list[UserSchema])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await user_crud.get_all_users(db)


# ✅ 특정 유저 조회 (자기 자신만 조회 가능하도록 제한 가능)
@router.get("/{user_id}", response_model=UserSchema)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    user = await user_crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user


# ✅ 유저 수정 (본인만 가능하도록 제한)
@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    user_update: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    db_user = await user_crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated = await user_crud.update_user(db, db_user, user_update)
    return UserSchema.model_validate(updated)


# ✅ 유저 삭제 (본인만 가능하도록 제한)
@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    db_user = await user_crud.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user_crud.delete_user(db, db_user)
    return {"message": "User deleted successfully"}
