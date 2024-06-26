from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import models,database
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    is_delete = Column(Boolean,default=False,nullable=False)

    blogs = relationship('Blog', back_populates="creator",cascade="all, delete")
class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    body = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    creator = relationship("User", back_populates="blogs")






# Base.metadata.create_all(bind=database.engine)



    

    




