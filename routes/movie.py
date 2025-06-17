from typing import List
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Movie, Janre
from sqlalchemy.orm import Session
from auth import require_level
import pyd

mov_router = APIRouter(
    prefix="/movies",
    tags=["movie"],
    responses={404: {"description": "Not found"}},
)


from sqlalchemy import select


@mov_router.get("", response_model=List[pyd.MovieResponse])
def read_movie(
    page: int = 1,
    limit: int = 10,
    genre: str = "",
    minRating: float = 0.0,
    session: Session = Depends(get_db),
):

    limit = min(limit, 100)
    offset = (page - 1) * limit
    result = (
        session.query(Movie)
        .join(Movie.janre)
        .filter(Movie.rating >= minRating)
        .filter(Movie.janre.has(Janre.name.ilike(f"%{genre}%")))
        .order_by(Movie.rating.desc())
        .limit(limit)
        .offset(offset)
    )
    if result.count() == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No movies found.",
        )

    movs = session.execute(result).scalars().all()

    return movs


@mov_router.get("/{movie_id}", response_model=pyd.MovieResponse)
def read_movie_id(movie_id: int, session: Session = Depends(get_db)):
    result = session.execute(select(Movie).where(Movie.id == movie_id))
    mov = result.scalars().first()
    if not mov:
        raise HTTPException(
            status_code=404,
            detail=f"Movie with id '{movie_id}' does not exist.",
        )
    return mov


@mov_router.post("", response_model=pyd.MovieResponse)
def create_movie(
    movie: pyd.CreateMovie,
    session: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):

    exist_mov = session.execute(select(Movie).where(Movie.name == movie.name))
    if exist_mov.first():
        raise HTTPException(
            status_code=400,
            detail=f"Movie with name '{movie.name}' already exists.",
        )

    exist_janre = (
        session.execute(select(Janre).where(Janre.name == movie.janre))
        .scalars()
        .first()
    )

    if not exist_janre:
        exist_janre = Janre(name=movie.janre)
        session.add(exist_janre)
        session.commit()
        session.refresh(exist_janre)

    new_movie = Movie(
        name=movie.name,
        janre_id=exist_janre.id,
        duration_min=movie.duration_min,
        rating=movie.rating,
    )
    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)
    return new_movie


@mov_router.put("/{movie_id}", response_model=pyd.MovieResponse)
def update_movie(
    movie_id: int,
    movie: pyd.UpdateMovie,
    session: Session = Depends(get_db),
    usr=Depends(require_level(3)),
):
    exist_mov = (
        session.execute(select(Movie).where(Movie.id == movie_id)).scalars().first()
    )
    if not exist_mov:
        raise HTTPException(
            status_code=404,
            detail=f"Movie with id '{movie_id}' does not exist.",
        )
    exist_janre = None
    if movie.janre:
        exist_janre = (
            session.execute(select(Janre).where(Janre.name == movie.janre))
            .scalars()
            .first()
        )
        if not exist_janre:
            raise HTTPException(
                status_code=400,
                detail=f"Janre with name '{movie.janre}' does not exist.",
            )
    exist_mov.name = movie.name
    exist_mov.duration_min = movie.duration_min
    exist_mov.rating = movie.rating

    if exist_janre:
        exist_mov.janre_id = exist_janre.id

    session.commit()
    session.refresh(exist_mov)
    return exist_mov


@mov_router.delete("/{movie_id}", response_model=str)
def delete_movie(
    movie_id: int, session: Session = Depends(get_db), usr=Depends(require_level(3))
):
    exist_mov = (
        session.execute(select(Movie).where(Movie.id == movie_id)).scalars().first()
    )
    if not exist_mov:
        raise HTTPException(
            status_code=404,
            detail=f"Movie with id '{movie_id}' does not exist.",
        )
    session.delete(exist_mov)
    session.commit()
    return f"Deleted movie with id {movie_id}."
