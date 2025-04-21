from fastapi import FastAPI, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from pyd.schemas import ResponseMovie

app=FastAPI()

@app.get("/movies", response_model=List[ResponseMovie])
def get_movies(
    db:Session=Depends(get_db)
):
    movies = db.query(m.Movie).all()
    return movies

@app.get("/movie/{id}")
def get_mov_by_id(id: )
