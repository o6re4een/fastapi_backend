from pydantic import BaseModel, Field


class BaseMovie(BaseModel):

    id: int
    name: str
    release_year: int

    rating: float
    description: str | None
    poster: str | None
    date_created: str


class EditMovie(BaseModel):
    name: str
    release_year: int

    rating: float
    description: str | None
    poster: str | None
    date_created: str


class BaseJanre(BaseModel):
    id: int
    name: str
    description: str | None
