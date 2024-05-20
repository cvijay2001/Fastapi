from pydantic import BaseModel ,EmailStr
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
        from_attributes = True


class UserBase(BaseModel):
    id:int
    username:str
    # email:EmailStr
    email:str

class UserEmailOnly(BaseModel):
    email :EmailStr
    

class User(BaseModel):
    username:str 
    password:str
    # email:EmailStr
    email=str
    # role:str

class ShowUser(BaseModel):
    # id:int
    username:str
    # email:EmailStr
    email:str
    tasks : List[Task] =[]

    
    class Config():
        from_attributes = True

class ShowUserWithId(ShowUser):
    id:int
    class Config():
        from_attributes = True
        
class ShowUserwithDeleteFlag(ShowUserWithId):
    role:str
    is_delete:bool
    class Config():
        from_attributes = True

class ShowtaskUser(BaseModel):
    username:str
    email:EmailStr
    # role:str

class ShowTask(BaseModel):
    id:int
    title: str
    description:str
    due_date:date
    status: str
    creator: ShowtaskUser

    class Config():
        from_attributes = True

class Login(BaseModel):
    username:str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None