from typing import List
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Role
from sqlalchemy.orm import Session
from auth import require_level
import pyd

role_router = APIRouter(
    prefix="/role",
    tags=["role"],
    responses={404: {"description": "Not found"}},
)


from sqlalchemy import select


@role_router.get("", response_model=List[pyd.RoleResponse])
async def read_roles(
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):
    offset = (page - 1) * limit
    query = select(Role).offset(offset).limit(limit)
    res = db.execute(query).scalars().all()
    return res


@role_router.post("", response_model=pyd.RoleResponse)
async def create_role(
    role: pyd.CreateRole,
    db: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@role_router.put("/{id}", response_model=pyd.RoleResponse)
async def update_role(
    id: int,
    role: pyd.CreateRole,
    db: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):
    db_role = db.query(Role).filter(Role.id == id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    db_role.name = role.name
    db.commit()
    db.refresh(db_role)

    return db_role


@role_router.get("/{id}", response_model=pyd.RoleResponse)
async def read_role(
    id: int, db: Session = Depends(get_db), usr=Depends(require_level(3))
):
    db_role = db.query(Role).filter(Role.id == id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role
