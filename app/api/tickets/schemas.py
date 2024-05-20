from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


class TicketBase(BaseModel):
    ticket_type: str = Field(..., description="Type of the ticket (e.g., VIP, General Admission)")
    price: float = Field(..., description="Price of the ticket")
    quantity: int = Field(..., description="Number of tickets available", gt=0)

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    pass

class TicketInDBBase(TicketBase):
    id: int
    event_id: int

    class Config:
        from_attributes = True

class Ticket(TicketInDBBase):
    pass

class TicketInDB(TicketInDBBase):
    pass