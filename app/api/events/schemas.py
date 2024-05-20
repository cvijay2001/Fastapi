from typing import Optional
from pydantic import BaseModel
from datetime import date

class EventBase(BaseModel):
    title: str
    description: str
    date: date
    location: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    class Config:
        from_attributes = True
