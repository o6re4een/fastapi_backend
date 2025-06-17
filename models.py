from datetime import datetime
from typing import List
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float, DateTime
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

# association_table = Table(
#     "janre_movie",
#     Base.metadata,
#     Column("movie_id", ForeignKey("movies.id"), primary_key=True),
#     Column("janre_id", ForeignKey("janres.id"), primary_key=True),
# )


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    duration_min = Column(Integer)
    rating = Column(Float, default=0)

    janre: Mapped["Janre"] = relationship(back_populates="movies")
    janre_id = Column(Integer, ForeignKey("janres.id"), nullable=False)
    sessions: Mapped[List["Session"]] = relationship(back_populates="movie")
    reviews: Mapped[List["Review"]] = relationship(back_populates="movie")


class Janre(Base):
    __tablename__ = "janres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    movies: Mapped[List[Movie]] = relationship(back_populates="janre")


class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sessions: Mapped[List["Session"]] = relationship(back_populates="place")


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    place_num = Column(Integer)

    user: Mapped["User"] = relationship(back_populates="tickets")
    session: Mapped["Session"] = relationship(back_populates="tickets")


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    time = Column(DateTime)
    price = Column(Float)

    place: Mapped["Place"] = relationship(back_populates="sessions")
    movie: Mapped["Movie"] = relationship(back_populates="sessions")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="session")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    movie: Mapped["Movie"] = relationship(back_populates="reviews")
    user: Mapped["User"] = relationship(back_populates="reviews")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship("User", back_populates="role")
    level = Column(Integer, nullable=False, default=1)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)

    first_name = Column(String)
    last_name = Column(String)
    sur_name = Column(String)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", back_populates="users")
    reviews = relationship("Review", back_populates="user")
    tickets = relationship("Ticket", back_populates="user")
