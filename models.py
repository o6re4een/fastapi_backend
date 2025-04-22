from datetime import datetime
from typing import List
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship, Mapped

# class Car(Base): #N
#     __tablename__ = "cars"

#     id=Column(Integer,primary_key=True,index=True)
#     brand=Column(String)
#     model=Column(String)
#     yearofproduction=Column(Integer)
#     category_id=Column(Integer,ForeignKey("categories.id"))
#     category=relationship("Category",backref="cars")
# class Category(Base): #1
#     __tablename__ = "categories"

#     id=Column(Integer,primary_key=True,index=True)
#     type=Column(String)

association_table = Table(
    "janre_movie",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("janre_id", ForeignKey("janres.id"), primary_key=True),
)


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    release_year = Column(Integer)
    janres: Mapped[List["Janre"]] = relationship(
        secondary=association_table, back_populates="movies"
    )
    duration_min = Column(Integer)
    rating = Column(Float)
    description = Column(String, nullable=True)
    poster = Column(String, nullable=True)
    date_created = Column(String, default=datetime.now)


class Janre(Base):
    __tablename__ = "janres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    movies: Mapped[List[Movie]] = relationship(
        secondary=association_table, back_populates="janres"
    )
