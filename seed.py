from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import engine
import models as m
from auth import get_password_hash

# Очистка и пересоздание базы
m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)


def get_default_password(n: int | None):
    if n == 1:
        return get_password_hash("admin")
    elif n == 2:
        return get_password_hash("cash")
    else:
        return get_password_hash("user")


with Session(bind=engine) as session:
    # Роли
    roles = [
        m.Role(name="user", level=1),
        m.Role(name="cashier", level=2),
        m.Role(name="admin", level=3),
    ]
    session.add_all(roles)
    session.commit()

    # Пользователи
    users = [
        m.User(
            email="admin@site.com",
            password=get_default_password(1),
            first_name="Alice",
            last_name="Adminova",
            sur_name="A.",
            role=roles[2],
        ),
        m.User(
            email="bob@site.com",
            password=get_default_password(3),
            first_name="Bob",
            last_name="Bobov",
            sur_name="B.",
            role=roles[0],
        ),
        m.User(
            email="clara@site.com",
            password=get_default_password(3),
            first_name="Clara",
            last_name="Clarova",
            sur_name="C.",
            role=roles[0],
        ),
        m.User(
            email="mod@site.com",
            password=get_default_password(2),
            first_name="Mick",
            last_name="Mod",
            sur_name="M.",
            role=roles[1],
        ),
    ]
    session.add_all(users)
    session.commit()

    # Жанры
    janres = [
        m.Janre(name="Action", description="Динамичные боевики"),
        m.Janre(name="Comedy", description="Юмористические фильмы"),
        m.Janre(name="Drama", description="Серьезные драмы"),
        m.Janre(name="Sci-Fi", description="Научная фантастика"),
    ]
    session.add_all(janres)
    session.commit()

    # Фильмы
    movies = [
        m.Movie(
            name="Avengers: Endgame", duration_min=181, rating=9.0, janre=janres[0]
        ),
        m.Movie(name="Interstellar", duration_min=169, rating=8.6, janre=janres[3]),
        m.Movie(name="The Godfather", duration_min=175, rating=9.2, janre=janres[2]),
        m.Movie(name="Superbad", duration_min=113, rating=7.6, janre=janres[1]),
    ]
    session.add_all(movies)
    session.commit()

    # Места
    places = [
        m.Place(name="Cinema City"),
        m.Place(name="MegaCinema"),
        m.Place(name="Luxor"),
    ]
    session.add_all(places)
    session.commit()

    # Сеансы
    now = datetime.now()
    sessions = [
        m.Session(
            movie=movies[0], place=places[0], time=now + timedelta(days=1), price=550
        ),
        m.Session(
            movie=movies[1], place=places[1], time=now + timedelta(days=2), price=600
        ),
        m.Session(
            movie=movies[2], place=places[2], time=now + timedelta(days=3), price=500
        ),
        m.Session(
            movie=movies[3], place=places[0], time=now + timedelta(days=4), price=450
        ),
    ]
    session.add_all(sessions)
    session.commit()

    # Отзывы
    reviews = [
        m.Review(text="Лучший фильм года!", movie=movies[0], user=users[1]),
        m.Review(text="Очень глубокий сюжет", movie=movies[1], user=users[2]),
        m.Review(text="Классика!", movie=movies[2], user=users[1]),
        m.Review(text="Смешно, но местами глупо", movie=movies[3], user=users[2]),
    ]
    session.add_all(reviews)
    session.commit()

    # Билеты
    tickets = [
        m.Ticket(user_id=users[1].id, session_id=sessions[0].id, place_num=1),
        m.Ticket(user_id=users[2].id, session_id=sessions[0].id, place_num=2),
        m.Ticket(user_id=users[2].id, session_id=sessions[2].id, place_num=3),
        m.Ticket(user_id=users[3].id, session_id=sessions[1].id, place_num=4),
    ]
    session.add_all(tickets)
    session.commit()

    print("Сид завершён: база данных успешно заполнена.")
