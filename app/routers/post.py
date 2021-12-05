from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # posts = cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return posts # FastApi serializes the model into json

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()

#     return {"status": posts}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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

@router.get("/{id}")
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

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}")
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