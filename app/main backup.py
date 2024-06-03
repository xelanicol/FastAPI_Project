# cd app
# run in terminal: uvicorn main:app --reload

from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str # validation 
    content: str # validation
    published: bool = True # validation with default value if left blank
    # rating: Optional[int] = None # fully optional field, defaults to None, uses Optional module   

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

# GET path operation
# go to root/posts to get this!
@app.get("/posts") # if we put only "/" then it will go to the first method in the script with this path (root())
def get_posts():
    return {"data":my_posts}

# POST path operation
@app.post("/createposts", status_code=status.HTTP_201_CREATED) # HTTP POST method. NB. not best practice to do this
def create_posts(post: Post): #FastAPI will validate the input according to 'Post' class
    # print("Title = ", post.title)
    # print("Published = ",post.published)
    # print("Rating = ",post.rating)
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1_000_000_000) # give a fake ID randomly chosen
    my_posts.append(post_dict)
    return {"data":post_dict}

# GET/ID path operation
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # this line does the action of the following 2 lines
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {'post_detail':post}
    

@app.get("/posts/latest") # DOES NOT WORK, because it thinks it is using previous function, expecting int input
# if we moved before previous function it would work, but better to use different name
def get_latest_post():
    return my_posts[-1] # return newest post

# DELETE path operation
@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
            

# UPDATE path operation
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_dict = post.model_dump() # get dict
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}





