from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    rating:Optional[int] = None

# Works the same as extends in TypeScript
class CreatePost(PostBase):
    pass



