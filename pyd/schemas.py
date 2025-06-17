from typing import List, Optional

from pydantic import BaseModel, Field
from pyd.base_models import (
    BaseJanre,
    BaseMovie,
    BaseReview,
    BaseSession,
    BaseRole,
    BaseUser,
    BaseTicket,
    BasePlace,
)


class MovieResponse(BaseMovie):
    janre: BaseJanre
    reviews: List[BaseReview]
    sessions: List[BaseSession]


class PlaceResponse(BasePlace):

    sessions: List[BaseSession]


class SessionResponse(BaseSession):
    place: BasePlace
    movie: BaseMovie


class TicketResponse(BaseTicket):
    session: BaseSession
    user: BaseUser


class JanreResponse(BaseJanre):
    movies: List[BaseMovie]


class RoleResponse(BaseRole):
    users: List[BaseUser]

    class Config:
        from_attributes = True


class ReviewResponse(BaseReview):
    user: "UserReviewResponse"
    movie: BaseMovie


class UserResponse(BaseUser):
    role: BaseRole
    password: str = Field(exclude=True)


class UserReviewResponse(BaseModel):
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str
    access_token_expires: str
