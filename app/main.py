from fastapi import FastAPI
import yaml
from . import models
from .database import engine
from .routers import post, user, auth
from pydantic import BaseSettings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to my Python-based api!"}
