from fastapi import HTTPException,status
import models
import schemas
from sqlalchemy.orm import Session
from hashing import Hash
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
import traceback


def get_all_users(request, current_user: schemas.User, db: Session):
    # logger.info("Fetching all users from the database.")
    try:
        logger.info(f"request_method : {request.method} - /get_users/ API endpoint called by user: {current_user.username}")
        if current_user.role == "admin":
            users = db.query(models.User).filter(models.User.is_delete == False).all()
            logger.info(f" ia min get all users {users} ")
            if not users:
                # logger.warning("No users found.")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
            logger.success(f"All User {request.method} Successfull")
            return users
        else:
            logger.warning(f"Unauthorized access attempt by user : {current_user.username}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to access this endpoint")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error(f"An error occurred while fetching users: {str(e)} - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching users")
    
def create(user_data: schemas.User, db: Session,request):
    try:
        logger.info(f"request_method : {request.method} - API endpoint {'/create_user/'} called with the following username: {user_data.username}")
        user_exist = db.query(models.User).filter(models.User.username == user_data.username).first()
        if user_exist:
            logger.warning(f"Username already exists. username: {user_data.username}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

        db_user = models.User(username=user_data.username, email=user_data.email, password=Hash.get_password_hash(user_data.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.success(f"User created successfully {user_data.username}")
        return db_user
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error(f"An error occurred while creating user: {str(e)}  - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create user: Internal server error  ")

def get_one(request, id: int, db: Session):
    try:
        logger.info(f"request_method :{request.method} - API endpoint {'/create_user/'} called with the following data --> id:{id}")
        user_exists = db.query(models.User).filter(models.User.id == id).first()
        if not user_exists:
            logger.warning(f"No user Exists with id {id} to get data")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user present with id: {id}')
        logger.success(f"User data returned with data --> id {id}")
        return user_exists
    
    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"An error occurred while fetching user with data --> id {id}: {str(e)}  - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error occurred" )

def get_info(request,current_user,db:Session):
    try: 
        logger.info(f"request_method : {request.method} - /get_myinfo/ API endpoint called by user: {current_user.username}")
        if current_user.role in ("admin","regular"): 
            userinfo= db.query(models.User).filter(models.User.id == current_user.id).first()
        return userinfo
    except Exception as e:
        logger.error(f"request_method : {request.method} - /get_myinfo/  error -{e}  - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

def get_all_not_deleted(db:Session):
    all_users = db.query(models.User).filter(models.User.is_delete==False).all()
    print(all_users,"---------------< al users")
    if not all_users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return all_users

def delete_one(request, current_user, id: int, db: Session):
    try:
        logger.info(f"Request method: {request.method} - /delete_user/{id} API endpoint called by data: id:{id}")
        if current_user.role == "admin":
            user = db.query(models.User).filter(models.User.id == id, models.User.is_delete == False).first()
            if not user:
                logger.warning(f"No user present with id: {id} to delete")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user present with id: {id}')
            
            user.is_delete = True
            db.commit()
            db.refresh(user)
            logger.warning(f"User deleted with id: {id} to delete")
            return {'msg': 'User deleted successfully'}
        else:
            logger.error(f"Unauthorized access:user with id:{id} tried to delete the user who is not authorized ")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access: Only admin can delete users.")

    except HTTPException as http_exception:
        raise http_exception
    
    except Exception as e:
        logger.error(f"An error occurred while deleting user with id {id}: {str(e)} - {traceback.format_exc()}")


def partiallyupdate(request, userid, user_data, current_user, db):
    try:
        logger.info(f"Request method: {request.method} - /update_user/{userid} API endpoint called by data: id:{userid}")
        if current_user.role == "regular":
            updateUser = db.query(models.User).filter(and_(current_user.id == userid, 
                                                           models.User.id == current_user.id,
                                                           models.User.is_delete == False)).first()
        elif current_user.role == "admin":
            updateUser = db.query(models.User).filter(models.User.id == userid).first()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden : Need a authorize user to update users details")

        # Check if the user exists
        if not updateUser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No use exists with id : {userid} or you are not authorize to access this api")

        updateUser.email = user_data.email
        db.commit()
        logger.success(f"User : {userid} updated Successfully")
        db.refresh(updateUser)
        return updateUser

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        logger.error(f"An error occurred while partially updating user with id {userid}: {str(e)}  -  - {traceback.format_exc()}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error occurred")



def deleted_all_users(request,current_user, db):
    logger.info(f"Request method: {request.method} - /deleted_users/ API endpoint called by username: {current_user.username}")
    try:
        if current_user.role == "admin":
            deleted_users = db.query(models.User).filter(models.User.is_delete == True).all()
            if not deleted_users:
                logger.warning("No deleted users found")
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No deleted users found")
            else:
                logger.success("All Deleted Users Returned")
                return deleted_users
        else:
            logger.error(f"Tried Unauthorized access by user: {current_user.id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized access: Only admin users can access deleted users.")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        logger.error(f"An error occurred while retrieving deleted users: {str(e)} - {traceback.format_exc()}")
        # traceback.print_exc()  # Print traceback information
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error occurred")



    
