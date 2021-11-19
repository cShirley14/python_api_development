from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.datastructures import Default
from psycopg.rows import dict_row
from pydantic import BaseModel
import psycopg
import yaml
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

my_posts = [
    {
    "title": "Best Shoe Brands",
    "content": "Nike: Ranks as No. 1",
    "id": 1,
    },
    {
        "title": "Best Foods",
        "content": "Mom and Pop Shops appear to steal the show...",
        "id": 2
    }
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            print(p)
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if int(p['id']) == id:
            return i

@app.get("/")
def root():
    return {"message": "Welcome to my Python-based api!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # posts = cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return posts # FastApi serializes the model into json

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()

#     return {"status": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000000)
    # my_posts.append(post_dict)
    # return {"data": post_dict} 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content,
    #                         published=post.published)

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = (%s) """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message ' f"post with id: {id} not found :("}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found :(")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)): 
    # Deleting post
    # Find the index in the array that has req. ID
    # my_posts.pop(index)
    # index = find_index_post(id)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message ' f"post with id: {id} not found :("}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist") 

    post.delete(synchronize_session=False)

    db.commit()

    return post

@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # cursor.execute(""" UPDATE posts SET title= %s, content = %s, published = %s WHERE id = %sRETURNING * """, 
    #                 (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first() 