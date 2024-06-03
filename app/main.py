# cd app
# run in terminal: uvicorn main:app --reload

from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas #import from current dir
from .database import engine, get_db
from sqlalchemy.orm import Session
# create tables using SQLalchemy
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# from FASTAPI Documentation:

  

while True:
    try: # best to use try-except in case it fails
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi',
                                user = 'postgres', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)

my_posts = [
    {"title":"title of post 1", "content":"content of post 1", "id": 1},
    {"title":"favourite foods", "content":"I like pizza","id":2}            
] # for storing Post objects in memory

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# GET path operation / route
@app.get("/") # decorator: links the function to the FastAPI instance "app". GET is a HTTP method. "/" is root path.
def root(): # previously had 'async' before def, removed because optional
    return {"message":"Welcome to my *changed* API"} # FastAPI will convert this to JSON when sent to browser

# GET path operation (using raw SQL)
# go to root/posts to get this!
# @app.get("/posts") # if we put only "/" then it will go to the first method in the script with this path (root())
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data":posts}

# GET path operation (using ORM: sqlalchemy)
@app.get("/posts") # if we put only "/" then it will go to the first method in the script with this path (root())
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# POST path operation (raw SQL)
# @app.post("/createposts", status_code=status.HTTP_201_CREATED) # HTTP POST method. NB. not best practice to do this
# def create_posts(post: Post): #FastAPI will validate the input according to 'Post' class
#     # use of the %s format prevents 'SQL INJECTION' attacks
#     cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,
#                    vars=(post.title,post.content,post.published))
#     new_post = cursor.fetchone() # get input back
#     conn.commit() # commit changes to SQL database
#     return {"data":new_post}

# POST path operation (ORM: sqlalchemy)
@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump()) # unpack object-converted-to-dict to get all fields from object
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve new post (after defaults added)
    return new_post

# GET/ID path operation (raw SQL)
# @app.get("/posts/{id}")
# def get_post(id: str):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s """,vars=(str(id),)) # must convert to str
#     # comma in vars tuple seems necessary to prevent 500 error
#     post = cursor.fetchone()
#     print(post)
#     if not post:
#         # this line does the action of the following 2 lines
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'message': f"post with id: {id} was not found"}
#     return {'post_detail':post}

# GET/ID path operation (ORM: sqlalchemy)
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first() # need .all() or .first() to actually run SQL
    # we know there is just 1, so use .first() (because ID is unique)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post

# DELETE path operation (raw SQL)
# @app.delete("/posts/{id}")
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# DELETE path operation (ORM: sqlalchemy)
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first(): #if post doesn't exist
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    deleted_post = post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
            

# UPDATE path operation (raw SQL)
# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#                    (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")
#     return {"data":updated_post}

# UPDATE path operation (ORM: sqlalchemy)
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first(): #if post doesn't exist
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


