from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from database import get_db

import models as m


def get_janres(db: Session = Depends(get_db)):
    janres = db.query(m.Janre).all()
    return janres


def get_or_create_janre(db: Session = Depends(get_db), name=None):
    janre = db.query(m.Janre).filter(m.Janre.name == name).first()
    if janre is None:
        janre = m.Janre(name=name)
        db.add(janre)
        db.commit()
    return janre


def get_or_throw_janre(db: Session = Depends(get_db), name=None):
    janre = db.query(m.Janre).filter(m.Janre.name == name).first()
    if janre is None:
        raise HTTPException(status_code=404, detail=f"Janre not found: {name}")
    return janre
