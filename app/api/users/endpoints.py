# from api.auth import auth_schemas,auth_models
from sqlalchemy.orm import Session
from loguru import logger
from .helpers import user
import json
from fastapi import APIRouter, Depends, status, HTTPException,Request
from api.auth.oauth2 import get_current_user
from typing import List,Annotated
from sqlalchemy.orm import Session
from database import get_db
from . import schemas,models
from api.auth.basic_auth import get_current_username
# from routers import authentication
# from blog.repository import blog

router = APIRouter(
    prefix="/User",
    tags=['Users']
)

@router.post("/create_user/",status_code=status.HTTP_201_CREATED,response_model=schemas.User,description="This API is Used to Register a User")
def create_user(request: Request, user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    return user.create(user_data,db,request)

@router.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}

@router.get('/abc')
def getdata(username: Annotated[str, Depends(get_current_username)]):
    
    return {'msg':'i am from getdata'}


# @router.get("/get_users",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUserWithId])
# def get_users(request: Request, current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
#     # logger.info(f"API endpoint {'/create_user/'} :")
    
#     return user.get_all_users(request,current_user,db)
    
# @router.get("/get_myinfo/",status_code=status.HTTP_200_OK,response_model=schemas. UserBase)
# def get_myinfo(request:Request,current_user: Annotated[schemas.User, Depends(get_current_user)],db:Session = Depends(get_db)):
#     return user.get_info(request,current_user,db)


# @router.get("/get_user/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
# def get_user(request:Request,current_user: Annotated[schemas.User, Depends(get_current_user)],id:int ,db: Session = Depends(get_db)):
#     return user.get_one(request,id,db)

    

# @router.delete("/delete_user/{id}",status_code=status.HTTP_200_OK)
# def delete_user(request:Request,current_user: Annotated[schemas.User, Depends(get_current_user)],id:int,db:Session= Depends(get_db)):
#     return user.delete_one(request,current_user,id,db)
    

# @router.patch("/update_user/{userid}",status_code=status.HTTP_201_CREATED,response_model=schemas.UserBase)
# def update_user(request:Request, current_user: Annotated[schemas.User, Depends(get_current_user)], userid:int, user_data: schemas.UserEmailOnly, db: Session = Depends(get_db)):
#     return user.partiallyupdate(request,userid,user_data,current_user,db)

# @router.get("/deleted_users/",response_model=List[schemas.ShowUserwithDeleteFlag] )
# def deleted_user(request:Request,current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
#     # if not current_user.role == "admin":
#     #     return HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail={"Only admins are authorized"})
#     # else:
#     return user.deleted_all_users(request,current_user,db)
    
        