from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
import schemas
import database
from repository import user
# from blog.repository import blog

router = APIRouter(
    prefix="/User",
    tags=['Users']
)

get_db = database.get_db


@router.post("/create_user/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request,db)

@router.get("/get_users",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser])
def get_users( db: Session = Depends(get_db)):
    return user.get_all(db)
    


@router.get("/get_user/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
def get_user(id:int ,db: Session = Depends(get_db)):
    return user.get_one(id,db)