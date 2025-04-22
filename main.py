import os
import shutil
import uuid
from fastapi import FastAPI, HTTPException, Depends, Path, Query
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import Annotated, List
import pyd
from helpers import janres as j
from fastapi import FastAPI, File, UploadFile


MAX_FILE_SIZE_MB = 5
UPLOAD_DIR = "uploads"

app = FastAPI()


@app.get("/movies", response_model=List[pyd.ResponseMovie])
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(m.Movie).all()
    return movies


@app.get("/movie/{id}", response_model=pyd.ResponseMovie)
def get_mov_by_id(id: Annotated[int, Path(gt=0)], session: Session = Depends(get_db)):
    target_mov = session.query(m.Movie).filter_by(id=id).first()
    if not target_mov:
        raise HTTPException(status_code=404, detail="Movie not found")
    return target_mov


@app.post("/movies", response_model=pyd.ResponseMovie)
def create_movie(post_movie: pyd.CreateMovie, session: Session = Depends(get_db)):
    target_mov = session.query(m.Movie).filter_by(name=post_movie.name).first()
    if target_mov:
        raise HTTPException(status_code=400, detail="Movie already exists")
    new_movie = m.Movie()
    new_movie.name = post_movie.name
    new_movie.release_year = post_movie.release_year
    new_movie.rating = post_movie.rating
    new_movie.description = post_movie.description
    new_movie.duration_min = post_movie.duration_min
    for janre in post_movie.janres:

        target_janre = j.get_or_create_janre(session, janre)
        new_movie.janres.append(target_janre)
    if not new_movie.janres:
        raise HTTPException(
            status_code=400, detail="Movie must have at least one janre"
        )

    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)
    return new_movie


@app.put("/movies/img/{mov_id}", response_model=pyd.ResponseMovie)
def upload_movie_image(
    mov_id: Annotated[int, Path(gt=0)],
    file: UploadFile,
    session: Session = Depends(get_db),
):
    target_mov = session.query(m.Movie).filter_by(id=mov_id).first()
    if not target_mov:
        raise HTTPException(status_code=404, detail="Movie not found")
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format")

    file.file.seek(0, os.SEEK_END)  # Move to the end of the file
    size_mb = file.file.tell() / (1024 * 1024)  # Calculate size in MB
    file.file.seek(0)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File size exceeds limit")

    ext = file.filename.split(".")[-1]
    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(status_code=400, detail="Invalid image format")
    file_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    target_mov.poster = file_path
    session.commit()
    session.refresh(target_mov)
    return target_mov


@app.put("/movies/{mov_id}", response_model=pyd.ResponseMovie)
def update_movie(
    mov_id: Annotated[int, Path(gt=0)],
    movie: pyd.CreateMovie,
    db: Session = Depends(get_db),
):
    target_mov = db.query(m.Movie).filter_by(id=mov_id).first()
    if not target_mov:
        raise HTTPException(status_code=404, detail="Movie not found")

    target_mov.name = movie.name
    target_mov.release_year = movie.release_year
    target_mov.rating = movie.rating
    target_mov.description = movie.description
    target_mov.duration_min = movie.duration_min

    new_janres = []
    if movie.janres:

        for janre in movie.janres:
            if janre == "string":
                continue
            target_janre = j.get_or_throw_janre(db, janre)

            new_janres.append(target_janre)
    else:
        raise HTTPException(
            status_code=400, detail="Movie must have at least one janre"
        )
    target_mov.janres = new_janres
    db.commit()
    db.refresh(target_mov)
    return target_mov


@app.get("/janres")
def get_janres(db: Session = Depends(get_db)):
    janres = j.get_janres(db)
    if not janres:
        raise HTTPException(status_code=404, detail="Janres not found")
    return janres


@app.post("/janres", response_model=pyd.BaseJanre)
def create_janre(janre: pyd.CreateJanre, session: Session = Depends(get_db)):

    session.query(m.Janre).filter_by(name=janre.name).first()
    if session.query(m.Janre).filter_by(name=janre.name).first():
        raise HTTPException(status_code=400, detail="Janre already exists")
    session.add(janre)
    session.commit()
    session.refresh(janre)
    return janre


@app.delete("/movies/{mov_id}", response_model=dict[str, str])
def delete_movie(mov_id: int, db: Session = Depends(get_db)):
    target_mov = db.query(m.Movie).filter_by(id=mov_id).first()
    if not target_mov:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(target_mov)
    db.commit()
    return {"message": "Movie deleted successfully"}
