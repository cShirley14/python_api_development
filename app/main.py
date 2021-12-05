from fastapi import FastAPI
from psycopg.rows import dict_row
import psycopg
import yaml
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)

app.include_router(user.router)

with open('config.yaml', 'r') as file:
    raw_yml = yaml.load(file, Loader=yaml.SafeLoader)
    password = raw_yml["password"]
    user = raw_yml["user"]
    host = raw_yml["host"]
    dbname = raw_yml["dbname"]

# Connect to existing DB
try:
    conn = psycopg.connect(host=host , dbname=dbname , user=user, row_factory=dict_row, password=password)  
    cursor = conn.cursor()
    print("Database Connection was successful!")
except Exception as er:
    print("DB Connection Failure")
    print("ERROR: ", er)

@app.get("/")
def root():
    return {"message": "Welcome to my Python-based api!"}