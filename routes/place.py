from typing import List
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Place
from sqlalchemy.orm import Session
from auth import require_level
import pyd

place_router = APIRouter(
    prefix="/place",
    tags=["place"],
    responses={404: {"description": "Not found"}},
)


from sqlalchemy import select


@place_router.get("", response_model=List[pyd.PlaceResponse])
async def read_places(page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    query = select(Place).offset(offset).limit(limit)
    return db.execute(query).scalars().all()


@place_router.post("", response_model=pyd.PlaceResponse)
async def create_place(
    place: pyd.CreatePlace, db: Session = Depends(get_db), usr=Depends(require_level(3))
):
    db_place = Place(name=place.name)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


@place_router.put("/{id}", response_model=pyd.PlaceResponse)
async def update_place(
    id: int,
    place: pyd.CreatePlace,
    db: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):
    db_place = db.query(Place).filter(Place.id == id).first()
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    db_place.name = place.name
    db.commit()
    db.refresh(db_place)

    return db_place


@place_router.get("/{id}", response_model=pyd.PlaceResponse)
async def read_place(id: int, db: Session = Depends(get_db)):
    db_place = db.query(Place).filter(Place.id == id).first()
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return db_place


@place_router.delete("/{id}")
async def delete_place(
    id: int, db: Session = Depends(get_db), usr=Depends(require_level(3))
):
    db_place = db.query(Place).filter(Place.id == id).first()
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    db.delete(db_place)
    db.commit()
    return {"message": "Place deleted successfully"}
