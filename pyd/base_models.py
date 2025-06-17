import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class BaseModelCustom(BaseModel):
    date_create: str = Field(
        default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    date_update: str = Field(
        default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


class BaseMovie(BaseModelCustom):

    id: int
    name: str
    rating: float
    duration_min: int
    janre_id: int


class BasePlace(BaseModelCustom):
    id: int
    name: str


class BaseJanre(BaseModelCustom):
    id: int
    name: str
    description: str | None


class BaseTicket(BaseModelCustom):
    id: int
    user_id: int
    session_id: int
    place_num: int


class BaseSession(BaseModelCustom):
    id: int
    place_id: int
    time: datetime.datetime
    price: float
    movie_id: int


class BaseReview(BaseModelCustom):
    id: int
    text: str

    movie_id: int
    user_id: int


class BaseRole(BaseModel):
    id: int
    name: str


class BaseUser(BaseModel):
    id: int
    sur_name: str
    first_name: str
    last_name: str
    password: str
    role_id: int
    email: str
