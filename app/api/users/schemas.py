# auth/schemas.py
from enum import Enum
from pydantic import BaseModel,EmailStr
from enum import Enum as PyEnum


class GenderType(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class UserRole(str, PyEnum):
    admin = "admin"
    event_organizer = "event_organizer"
    regular_user = "regular_user"

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    gender: GenderType

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True


class Login(BaseModel):
    username:str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

