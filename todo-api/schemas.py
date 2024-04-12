from pydantic import BaseModel 
from typing import Union,List
from datetime import date


class TaskBase(BaseModel):
    title: str
    description:str
    due_date:date
    status: str

class Task(TaskBase):
    # user_id:int
    id:int 
    class Config():
        orm_mode = True


class UserBase(BaseModel):
    # id:str
    # username:str
    email:str
    

class User(BaseModel):
    username:str
    password:str
    email:str
    # role:str

class ShowUser(BaseModel):
    # id:int
    username:str
    email:str
    tasks : List[Task] =[]



class ShowUserWithId(ShowUser):
    id:int

class ShowUserwithDeleteFlag(ShowUserWithId):
    role:str
    is_delete:bool

class ShowtaskUser(BaseModel):
    username:str
    email:str
    # role:str

class ShowTask(BaseModel):
    title: str
    description:str
    due_date:date
    status: str
    creator: ShowtaskUser

    class Config():
        orm_mode = True

class Login(BaseModel):
    username:str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None