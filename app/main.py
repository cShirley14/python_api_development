from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel
from random import randrange
import psycopg
import yaml

app = FastAPI()

with open('config.yaml', 'r') as file:
    raw_yml = yaml.load(file, Loader=yaml.SafeLoader)
    password = raw_yml["password"]
    user = raw_yml["user"]
    host = raw_yml["host"]
    dbname = raw_yml["dbname"]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
def get_posts():
    return {"data": my_posts } 

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict} 

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message ' f"post with id: {id} not found :("}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found :(")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response): 
    # Deleting post
    # Find the index in the array that has req. ID
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message ' f"post with id: {id} not found :("}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist") 
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}