from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing_extensions import Annotated
from typing import Optional

# schema / Pydantic model - will do some validation for BODY of HTML request

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase): # class inheritance
    pass # if same as PostBase

class PostResponse(PostBase): # for containing response from server to user
    created_at: datetime
    owner_id: int
    id: int
    owner: UserOut

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int # Optional[str] = None

class Vote(BaseModel):
    vote_id: int
    dir: Annotated[int, Field(strict=True, le=1)] # restrict to 0, 1

class PostOut(BaseModel):
    Post: PostResponse
    votes: int