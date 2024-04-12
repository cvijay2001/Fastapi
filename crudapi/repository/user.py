from fastapi import HTTPException,status
import models
import schemas
from sqlalchemy.orm import Session
from hashing import Hash


def create(request: schemas.User, db: Session):
    db_user = models.User(name=request.name, email=request.email, password=Hash.get_password_hash(request.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_one(id:int,db:Session):
    single_user = db.query(models.User).filter(models.User.id == id).first()
    if not single_user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return single_user

def get_all(db:Session):
    all_users = db.query(models.User).filter(db.is_delete==False)
    if not all_users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return all_users

def delete_one(id:int,db:Session):
    single_user = db.query(models.User).filter(models.User.id == id).first()
    if not single_user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    single_user.is_delete = True
    db.commit()
    db.refresh(single_user)
    return {'msg': 'User deleted Successfully'}
    
