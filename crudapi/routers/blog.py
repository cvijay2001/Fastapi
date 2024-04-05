from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
import schemas
import database
from repository import blog
# from blog.repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

get_db = database.get_db


@router.get("/get_blogs/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])
def get_blogs(db:Session = Depends(get_db)):
    return blog.get_all(db)
    


@router.get("/get_blog/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
def get_blog(id:int,db:Session = Depends(get_db)):
    return blog.get_one(id,db)


@router.post("/create_blog/",status_code=status.HTTP_201_CREATED,response_model=schemas.Blog)
def get_blog(request:schemas.Blog,db:Session = Depends(get_db)):
    return blog.add_blog(request,db)