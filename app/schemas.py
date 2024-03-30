from fastapi.params import Body
from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    rating:Optional[int] = None

# Works the same as extends in TypeScript
class CreatePost(PostBase):
    pass

class UserResponseSchema (BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

class UpdatePost(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponseSchema
    

    # Use this class to return the data in the response
    # class config:
    #     orm_mode = True


#Users schema
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int]