from fastapi import HTTPException,status
import models
import schemas
from sqlalchemy.orm import Session
from hashing import Hash



def create(request: schemas.User, db: Session):
    user_exist = db.query(models.User).filter(models.User.username == request.username).first()
    if user_exist:
        raise HTTPException(status_code=status.allreadyexits)
    
    db_user = models.User(username=request.username, email=request.email, password=Hash.get_password_hash(request.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_one(id:int,db:Session):

    print( " in get_one funcion (id ,db:session )")

    user_exits= db.query(models.User).filter(models.User.id == id).first()
    if not user_exits :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return user_exits

def get_info(id:int,db:Session):
    print("--------------->in getifo functio")
    userinfo= db.query(models.User).filter(models.User.id == id).first()
    return userinfo

def get_all(db:Session):
    all_users = db.query(models.User).all()
    if not all_users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return all_users

def delete_one(id:int,db:Session):
    single_user = db.query(models.User).filter(models.User.id == id).first()
    if not single_user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    db.delete(single_user)
    db.commit()
    return {'msg': 'User deleted Successfully'}


def partiallyupdate(userid,request,current_user,db):

    print(" =------------>in partiallyupdate function")
    if current_user.role == "regular":
        updateUser = db.query(models.User).filter((current_user.id == userid) & (models.User.id == current_user.id)).first()
    elif current_user.role == "admin":
        updateUser = db.query(models.User).filter(models.User.id == userid).first()
    else:
        print("before formbidden")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Check if the user exists
    if not updateUser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    print("Before updating the email")
    # updateUser.username = request.username
    updateUser.email = request.email
    # updateUser.username = request.username

    db.commit()
    db.refresh(updateUser)
    return updateUser



    
