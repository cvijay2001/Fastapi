from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from oauth2 import get_current_user


# def is_admin(func):
#     """
#     Decorator to check if the current user is an admin.
#     """
#     async def wrapper(*args, **kwargs):
#         current_user = get_current_user()
#         if current_user.role != "admin":  # Assuming 'role' attribute exists in TokenData
#             raise HTTPException(status_code=403, detail="Not authorized, admin role required")
#         return current_user
#     return wrapper

# @is_admin
def get_all(db: Session):

    print("---------->in getall repository function")
    all_tasks = db.query(models.Task).all()

    print("alltasks --------------> ",all_tasks)
    
    if not all_tasks :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    print("before return all tasks --------------->>>")
    return all_tasks

def get_one(id:int,db: Session):
    single_blog = db.query(models.Task).filter(models.Task.id == id).first()
    if not single_blog :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
    return single_blog

def add_task(request: schemas.Task, db: Session,c_user):
    addTask = models.Task(title=request.title,description=request.description,due_date=request.due_date,status=request.status,user_id=c_user.id)
    db.add(addTask)
    db.commit()
    db.refresh(addTask)
    return addTask

def update_one(task_id, request, db, current_user):
    # Check if the user is an admin or regular user
    if current_user.role == "regular":
        update_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    elif current_user.role == "admin":
        update_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    # Check if the task exists
    if not update_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task with ID {task_id} found")

    # Update the task with the new data
    update_task.title = request.title
    update_task.description = request.description
    update_task.due_date = request.due_date
    update_task.status = request.status

    # Commit the changes to the database
    db.commit()

    # Refresh the task to get the updated values
    db.refresh(update_task)

    return update_task
