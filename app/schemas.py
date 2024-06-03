from pydantic import BaseModel

# schema / Pydantic model - will do some validation for BODY of HTML request


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase): # class inheritance
    pass # if same as PostBase