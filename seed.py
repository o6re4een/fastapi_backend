from datetime import datetime
from sqlalchemy.orm import Session
from database import engine
import models as m


m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    # Создаем жанры
    janres = [
        m.Janre(
            name="Боевик",
            description="Фильмы с динамичными сценами борьбы, погонями и перестрелками"
        ),
        m.Janre(
            name="Комедия",
            description="Юмористические фильмы, предназначенные для развлечения"
        ),
        m.Janre(
            name="Драма",
            description="Серьезные фильмы с глубоким сюжетом и эмоциональной игрой актеров"
        ),
        m.Janre(
            name="Фантастика",
            description="Фильмы с элементами научной фантастики и футуристическими технологиями"
        ),
        m.Janre(
            name="Ужасы",
            description="Фильмы, предназначенные для того, чтобы напугать зрителя"
        ),
    ]
    session.add_all(janres)
    session.commit()

    # Создаем фильмы
    movies = [
        m.Movie(
            name="Крепкий орешек",
            release_year=1988,
            duration_min=132,
            rating=8.2,
            description="Полицейский пытается спасти людей, взятых в заложники террористами в небоскребе",
            poster="https://example.com/diehard.jpg",
            janres=[janres[0], janres[2]]  # Боевик и немного комедии
        ),
        m.Movie(
            name="Назад в будущее",
            release_year=1985,
            duration_min=116,
            rating=8.5,
            description="Подросток случайно отправляется в прошлое на машине времени",
            poster="https://example.com/backtothefuture.jpg",
            janres=[janres[3], janres[2]]  # Фантастика и комедия
        ),
        m.Movie(
            name="Зеленая миля",
            release_year=1999,
            duration_min=189,
            rating=9.1,
            description="История о надзирателе тюрьмы и необычном заключенном",
            poster="https://example.com/greenmile.jpg",
            janres=[janres[2], janres[3]]  # Драма и элементы фантастики
        ),
        m.Movie(
            name="Оно",
            release_year=2017,
            duration_min=135,
            rating=7.3,
            description="Группа детей сталкивается с древним злом в своем городке",
            poster="https://example.com/it.jpg",
            janres=[janres[4]]  # Ужасы
        ),
        m.Movie(
            name="Достать ножи",
            release_year=2019,
            duration_min=130,
            rating=7.9,
            description="Детектив расследует смерть богатого писателя",
            poster="https://example.com/knivesout.jpg",
            janres=[janres[1], janres[2]]  # Комедия и драма
        ),
    ]
    session.add_all(movies)
    session.commit()

    print("Данные успешно добавлены в базу!")