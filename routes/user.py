from typing import List
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import User
from sqlalchemy.orm import Session
from auth import require_level
import pyd

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


from sqlalchemy import select


@user_router.get("", response_model=List[pyd.UserResponse])
async def read_users(
    email: str = "",
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):
    offset = (page - 1) * limit
    if email != "":
        query = (
            select(User)
            .where(User.email.like(f"%{email}%"))
            .limit(limit)
            .offset(offset)
        )
    else:
        query = select(User).limit(limit).offset(offset)
    return db.execute(query).scalars().all()


@user_router.get("/me", response_model=pyd.UserResponse)
async def read_user_me(usr=Depends(require_level(1))):
    return usr


@user_router.get("/{user_id}", response_model=pyd.UserResponse)
async def read_user(
    user_id: int, db: Session = Depends(get_db), usr=Depends(require_level(3))
):
    query = select(User).where(User.id == user_id)
    result = db.execute(query).scalars().first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@user_router.put("", response_model=pyd.UserResponse)
async def update_user(
    upd_user: pyd.UpdateUser,
    db: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):

    query = select(User).where(User.id == upd_user.id)
    user = db.execute(query).scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = upd_user.email
    user.first_name = upd_user.first_name
    user.last_name = upd_user.last_name
    user.sur_name = upd_user.sur_name
    user.role_id = upd_user.role_id
    db.commit()
    db.refresh(user)
    return user


@user_router.delete("/{user_id}", response_model=pyd.UserResponse)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):

    query = select(User).where(User.id == user_id)
    user = db.execute(query).scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
