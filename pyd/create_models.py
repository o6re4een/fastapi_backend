from typing import Annotated, List
from pydantic import BaseModel, Field
from sqlalchemy import String
from pyd.base_models import BaseJanre


class CreateJanre(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class CreateMovie(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(
        ...,
        min_length=0,
        max_length=50,
    )
    release_year: int = Field(..., gt=1900, lt=2100)
    rating: float = Field(..., gt=0, lt=10)
    janres: list[Annotated[str, Field(..., min_length=3, max_length=50)]]
    duration_min: int = Field(..., gt=0)
