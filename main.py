from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

