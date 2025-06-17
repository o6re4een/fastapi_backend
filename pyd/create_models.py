import datetime
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from sqlalchemy import String
from pyd.base_models import BaseJanre


class CreateJanre(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=3, max_length=50)


class CreatePlace(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)


class CreateMovie(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    duration_min: int = Field(..., gt=0)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    janre: str = Field(..., min_length=3, max_length=50)


class CreateTicket(BaseModel):
    user_id: int = Field(..., gt=0)
    session_id: int = Field(..., gt=0)
    place_num: int = Field(..., gt=0)


class CreateUser(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=50)
    password_repreat: str = Field(..., min_length=3, max_length=50)

    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    sur_name: str = Field(..., min_length=3, max_length=50)

    @field_validator("password_repreat", mode="after")
    def passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if value != info.data["password"]:
            raise ValueError("Passwords do not match")
        return value

    @field_validator("email")
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("Invalid email address")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")

        return value


class CreateSession(BaseModel):
    movie_id: int = Field(..., gt=0)
    place_id: int = Field(..., gt=0)
    time: datetime.datetime
    price: int = Field(..., gt=0)


class CreateRole(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)


class CreateReview(BaseModel):
    text: str = Field(..., min_length=3, max_length=4096)
    movie_id: int = Field(..., gt=0)
