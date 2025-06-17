from typing import List
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Movie, Review
from sqlalchemy.orm import Session, joinedload
from auth import require_level, get_current_user
import pyd

review_router = APIRouter(
    prefix="/review",
    tags=["review"],
    responses={404: {"description": "Not found"}},
)


from sqlalchemy import select


@review_router.get("", response_model=List[pyd.ReviewResponse])
async def read_reviews(
    movie: str = "",
    page: int = 1,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    # Базовый запрос: тянем Review вместе с фильмом
    query = select(Review).options(joinedload(Review.movie))

    # Если есть фильтр по названию фильма — добавляем WHERE через .has()
    if movie:
        # добавляем wildcard, чтобы ilike работал как "%movie%"
        query = query.where(Review.movie.has(Movie.name.ilike(f"%{movie}%")))

    # Сортировка, пагинация
    query = query.order_by(Review.id)
    offset = (page - 1) * limit
    query = query.limit(limit).offset(offset)

    # Выполняем
    res = db.execute(query).scalars().all()
    return res


@review_router.post("", response_model=pyd.ReviewResponse)
async def create_review(
    review: pyd.CreateReview,
    db: Session = Depends(get_db),
    usr=Depends(require_level(1)),
):
    db_review = Review(text=review.text, movie_id=review.movie_id, user_id=usr.id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@review_router.put("/{id}", response_model=pyd.ReviewResponse)
async def update_review(
    id: int,
    review: pyd.UpdateReview,
    db: Session = Depends(get_db),
    usr=Depends(require_level(1)),
):

    db_review = db.query(Review).filter(Review.id == id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    if usr.id != db_review.user_id and usr.role.name != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    db_review.text = review.text

    db.commit()
    db.refresh(db_review)
    return db_review


@review_router.get("/{id}", response_model=pyd.ReviewResponse)
async def read_review(
    id: int, db: Session = Depends(get_db), usr=Depends(require_level(1))
):
    db_review = db.query(Review).filter(Review.id == id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review


@review_router.delete("/{id}", response_model=str)
async def delete_review(
    id: int,
    db: Session = Depends(get_db),
    usr=Depends(require_level(1)),
):
    db_review = db.query(Review).filter(Review.id == id).first()
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    if usr.id != db_review.user_id and usr.role.name != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(db_review)
    db.commit()
    return "deleted"
