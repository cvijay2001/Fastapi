from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status


def get_all(db: Session):
    all_blogs = db.query(models.Blog).all()
    if not all_blogs :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return all_blogs

def get_one(id:int,db: Session):
    single_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not single_blog :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return single_blog

def add_blog(request: schemas.Blog, db: Session):
    add_blog = models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    db.add(add_blog)
    db.commit()
    db.refresh(add_blog)
    return add_blog