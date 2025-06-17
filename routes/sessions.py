import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from auth import require_level
from database import get_db
from models import Session as SM, Movie, Place
from sqlalchemy.orm import Session

import pyd

session_router = APIRouter(
    prefix="/session",
    tags=["session"],
    responses={404: {"description": "Not found"}},
)


from sqlalchemy import select


@session_router.get("", response_model=List[pyd.SessionResponse])
async def read_sessions(
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
    usr=Depends(require_level(2)),
):
    offset = (page - 1) * limit
    query = select(SM).offset(offset).limit(limit)
    return db.execute(query).scalars().all()


@session_router.post("", response_model=pyd.SessionResponse)
async def create_session(
    session_n: pyd.CreateSession,
    db: Session = Depends(get_db),
    usr=Depends(require_level(2)),
):

    valdiate_session(session_n, db)

    db_session = SM(**session_n.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@session_router.put("/{id}", response_model=pyd.SessionResponse)
async def update_session(
    id: int,
    session_n: pyd.CreateSession,
    db: Session = Depends(get_db),
    usr=Depends(require_level(2)),
):
    valdiate_session(session_n, db)

    db_session = db.query(SM).filter(SM.id == id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="session not found")
    db_session.price = session_n.price
    db_session.movie_id = session_n.movie_id
    db_session.place_id = session_n.place_id
    db_session.time = session_n.time

    db.commit()
    db.refresh(db_session)

    return db_session


@session_router.get("/{id}", response_model=pyd.SessionResponse)
async def read_session(
    id: int, db: Session = Depends(get_db), usr=Depends(require_level(2))
):
    db_session = db.query(SM).filter(SM.id == id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="session not found")
    return db_session


@session_router.delete("/{id}")
async def delete_session(
    id: int, db: Session = Depends(get_db), usr=Depends(require_level(2))
):
    db_session = db.query(SM).filter(SM.id == id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="session not found")
    db.delete(db_session)
    db.commit()
    return {"ok": True}


def valdiate_session(session_n: pyd.CreateSession, db: Session):
    if session_n.price <= 0:
        raise HTTPException(status_code=400, detail="price not valid")

    if session_n.time < datetime.datetime.now(datetime.timezone.utc):
        raise HTTPException(status_code=400, detail="time not valid")

    exist_mov = db.query(Movie).filter(Movie.id == session_n.movie_id).first()
    if not exist_mov:
        raise HTTPException(status_code=404, detail="movie not found")

    exist_place = db.query(Place).filter(Place.id == session_n.place_id).first()
    if not exist_place:
        raise HTTPException(status_code=404, detail="place not found")
    return
