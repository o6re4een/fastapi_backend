import os
import shutil
import uuid
from fastapi import APIRouter, FastAPI, HTTPException, Depends, Path, Query
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import Annotated, List
import pyd
from fastapi import FastAPI, File, UploadFile

from routes import (
    mov_router,
    place_router,
    session_router,
    ticket_router,
    janre_router,
    role_router,
    auth_router,
    review_router,
    user_router,
)


app = FastAPI(root_path="/api")


app.include_router(mov_router)
app.include_router(place_router)
app.include_router(session_router)
app.include_router(ticket_router)
app.include_router(janre_router)
app.include_router(role_router)
app.include_router(auth_router)
app.include_router(review_router)
app.include_router(user_router)
