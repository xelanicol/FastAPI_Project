from typing import Optional, List
from .. import models, schemas, oauth2
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

# GET path operation (using raw SQL)
# go to root/posts to get this!
# @app.get("/posts") # if we put only "/" then it will go to the first method in the script with this path (root())
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data":posts}

# GET path operation (using ORM: sqlalchemy)
@router.get("/",response_model=List[schemas.PostOut]) # removed /posts because added prefix to router object at start -> saves typing
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
    limit: int = 3, skip: int = 0, search: Optional[str] = ""):
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all() # left inner join by default

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
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) # unpack object-converted-to-dict to get all fields from object
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # retrieve new post (after defaults added)
    return new_post

# GET/ID path operation (raw SQL)s
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
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # need .all() or .first() to actually run SQL
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # we know there is just 1, so use .first() (because ID is unique)
    return post
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
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
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post: #if post doesn't exist
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
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
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()
    if not old_post: #if post doesn't exist
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if old_post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()