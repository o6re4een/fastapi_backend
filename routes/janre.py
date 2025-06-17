from typing import List
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Janre
from sqlalchemy.orm import Session
from auth import require_level
import pyd

janre_router = APIRouter(
    prefix="/janre",
    tags=["janre"],
    responses={404: {"description": "Not found"}},
)


from sqlalchemy import select


@janre_router.get("", response_model=List[pyd.JanreResponse])
async def read_janres(page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    query = select(Janre).offset(offset).limit(limit)
    return db.execute(query).scalars().all()


@janre_router.post("", response_model=pyd.JanreResponse)
async def create_janre(
    janre: pyd.CreateJanre, db: Session = Depends(get_db), usr=Depends(require_level(3))
):
    validate_janre(janre, db)
    db_janre = Janre(name=janre.name, description=janre.description)
    db.add(db_janre)
    db.commit()
    db.refresh(db_janre)
    return db_janre


@janre_router.put("/{id}", response_model=pyd.JanreResponse)
async def update_janre(
    id: int,
    janre: pyd.CreateJanre,
    db: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):

    db_janre = db.query(Janre).filter(Janre.id == id).first()
    if db_janre is None:
        raise HTTPException(status_code=404, detail="Janre not found")
    db_janre.name = janre.name
    db_janre.description = janre.description
    db.commit()
    db.refresh(db_janre)

    return db_janre


@janre_router.get("/{id}", response_model=pyd.JanreResponse)
async def read_janre(
    id: int,
    db: Session = Depends(get_db),
):
    db_janre = db.query(Janre).filter(Janre.id == id).first()
    if db_janre is None:
        raise HTTPException(status_code=404, detail="Janre not found")
    return db_janre


@janre_router.delete("/{id}", response_model=pyd.JanreResponse)
async def delete_janre(
    id: int, db: Session = Depends(get_db), usr=Depends(require_level(3))
):
    db_janre = db.query(Janre).filter(Janre.id == id).first()
    if db_janre is None:
        raise HTTPException(status_code=404, detail="Janre not found")
    db.delete(db_janre)
    db.commit()
    return db_janre


def validate_janre(janre: pyd.CreateJanre, db: Session):
    exist_janre = db.query(Janre).filter(Janre.name == janre.name).first()
    if exist_janre:
        raise HTTPException(status_code=400, detail="Janre already exists")
    return
