from pydantic import BaseModel, EmailStr
from datetime import datetime

# schema / Pydantic model - will do some validation for BODY of HTML request


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase): # class inheritance
    pass # if same as PostBase

class PostResponse(PostBase): # for containing response from server to user
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

