from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float
    desc: str