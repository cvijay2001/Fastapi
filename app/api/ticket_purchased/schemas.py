# # schemas.py

# from pydantic import BaseModel, Field
# from typing import Optional

# class TicketPurchaseBase(BaseModel):
#     ticket_id: int = Field(..., description="ID of the ticket to purchase")
#     quantity: int = Field(..., description="Number of tickets to purchase", gt=0)

# class TicketPurchaseCreate(TicketPurchaseBase):
#     pass

# class TicketPurchaseUpdate(TicketPurchaseBase):
#     pass

# class TicketPurchasedInDBBase(BaseModel):
#     id: int
#     quantity: int
#     ticket_id: int
#     user_id: int

#     class Config:
#         from_attributes = True

# class TicketPurchased(TicketPurchasedInDBBase):
#     pass

# class TicketPurchasedInDB(TicketPurchasedInDBBase):
#     pass


# schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TicketPurchaseBase(BaseModel):
    ticket_id: int = Field(..., description="ID of the ticket to purchase")
    quantity: int = Field(..., description="Number of tickets to purchase", gt=0)

class TicketPurchaseCreate(TicketPurchaseBase):
    pass

class TicketPurchaseUpdate(TicketPurchaseBase):
    pass

class TicketPurchasedInDBBase(BaseModel):
    id: int
    quantity: int
    ticket_id: int
    user_id: int

    class Config:
        from_attributes = True

class TicketPurchased(TicketPurchasedInDBBase):
    pass

class TicketPurchasedInDB(TicketPurchasedInDBBase):
    pass

class PurchasedTicketDetails(BaseModel):
    purchase_id: int
    quantity: int
    ticket_type: str
    ticket_price: float
    event_title: str
    event_date: date
    event_location: str

    class Config:
        from_attributes = True