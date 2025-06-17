from typing import Optional
from pydantic import BaseModel


class UpdateMovie(BaseModel):
    name: str
    rating: float
    duration_min: int
    janre: Optional[str] = None


class UpdateReview(BaseModel):
    text: str


class UpdateUser(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    sur_name: str
    role_id: int
