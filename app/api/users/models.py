
# auth/models.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Enum,ForeignKey,Date,Float, CheckConstraint
from database import Base
from .schemas import GenderType,UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=50), unique=True, index=True)  # Example length of 50 characters
    email = Column(String(length=100), unique=True, index=True) # Example length of 100 characters
    password_hash = Column(String(length=255))  # You can specify length here if needed
    role = Column(Enum(UserRole), default=UserRole.regular_user)
    full_name = Column(String(length=255), index=True)  # Example length of 255 characters
    gender = Column(Enum(GenderType))
    profile_pic = Column(String(length=255), nullable=True)  # Example length of 255 characters

    events = relationship("Event", back_populates="organizer", cascade="all, delete")
    ticket_purchases = relationship("TicketPurchased", back_populates="user", cascade="all, delete")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(255))
    date = Column(Date)
    location = Column(String(255))
    organizer_id = Column(Integer, ForeignKey("users.id"))
    # tickets_available = Column()
    organizer = relationship("User", back_populates="events")
    tickets = relationship('Ticket', back_populates='event',cascade='all, delete')


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    ticket_type = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer,CheckConstraint('quantity >= 0'))
    # quantity = Column(Integer)
    event_id = Column(Integer, ForeignKey('events.id'))

    event = relationship('Event', back_populates='tickets')
    purchased = relationship('TicketPurchased',back_populates='ticket',cascade='all, delete')


class TicketPurchased(Base):
    __tablename__ = 'ticket_purchased'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    user_id = Column(Integer,ForeignKey('users.id'))
    # ticket = relationship('Event', back_populates='tickets')
    user = relationship('User', back_populates='ticket_purchases')
    ticket = relationship('Ticket', back_populates='purchased')
    
