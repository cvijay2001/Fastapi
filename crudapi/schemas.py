from pydantic import BaseModel 
from typing import Union,List


class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    user_id:int
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str


class ShowUser(BaseModel):
    name:str
    email:str
    blogs : List[Blog] =[]
    class Config(): 
        orm_mode = True

class ShowblogUser(BaseModel):
    name:str
    email:str

class ShowBlog(BaseModel):
    title: str
    body:str
    creator: ShowblogUser

    class Config():
        orm_mode = True
