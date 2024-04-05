from fastapi import FastAPI, Depends, HTTPException,status,Response
from sqlalchemy.orm import Session
from typing import List
from models import User
import models
import database
from hashing import Hash
import schemas
from routers import blog,user

models.Base.metadata.create_all(bind=database.engine) 

app = FastAPI()

# Dependency to get the database session
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

app.include_router(blog.router)
app.include_router(user.router)





# ├── app
# │   ├── __init__.py
# │   ├── main.py
# │   ├── dependencies.py
# │   └── routers
# │   │   ├── __init__.py
# │   │   ├── items.py
# │   │   └── users.py
# │   └── internal
# │       ├── __init__.py
# │       └── admin.py








# @app.post("/create_user/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowUser)
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     db_user = models.User(name=request.name, email=request.email, password=request.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.get("/get_users",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowUser])
# def get_users( db: Session = Depends(get_db)):
#     all_users = db.query(User).all()
#     if not all_users :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
#     return all_users


# @app.get("/get_user/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowUser)
# def get_user(id:int ,db: Session = Depends(get_db)):
#     single_user = db.query(User).filter(User.id == id).first()
#     if not single_user :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
#     return single_user

# @app.get("/get_blogs/",status_code=status.HTTP_200_OK,response_model=List[schemas.ShowBlog])
# def get_blogs(db:Session = Depends(get_db)):
#     all_blogs = db.query(models.Blog).all()
#     if not all_blogs :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
#     return all_blogs
    


# @app.get("/get_blog/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
# def get_blog(id:int,db:Session = Depends(get_db)):
#     single_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not single_blog :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'NO User Present')
#     return single_blog








# # Create operation
# @app.post("/create_user/",status_code=status.HTTP_201_CREATED,response_model=ShowUserSchema)
# def create_user(user: UserSchema, db: Session = Depends(get_db)):
#     db_user = models.UserModel(username=user.username, email=user.email, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# Read operation
# @app.get("/students/",status_code=status.HTTP_200_OK)
# def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     students = db.query(models.StudentModel).offset(skip).limit(limit).all()
#     if not students:
#         Response.status_code = status.HTTP_404_NOT_FOUND
#     return students

# @app.get("/students/{student_id}")
# def read_student(student_id: int, db: Session = Depends(get_db)):
#     student = db.query(models.StudentModel).filter(models.StudentModel.id == student_id).first()
#     if student is None:
#         # Response.status_code = status.HTTP_404_NOT_FOUND
#         # return {f'details not found with {student_id} id'}
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'details not found with {student_id} id')
#     return student

# # Update operation 
# @app.put("/students/{student_id}", response_model=Student)
# def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):
#     db_student = db.query(models.StudentModel).filter(models.StudentModel.id == student_id).first()
#     if db_student is None:
#         raise HTTPException(status_code=404, detail="Student not found")
#     db_student.name = student.name
#     db_student.age = student.age
#     db_student.city = student.city
#     db.commit()
#     db.refresh(db_student)
#     return db_student

# # Delete operation
# @app.delete("/students/{student_id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_student(student_id: int, db: Session = Depends(get_db)):
#     db_student = db.query(models.StudentModel).filter(models.StudentModel.id == student_id)
#     if db_student is None:
#         raise HTTPException(status_code=404, detail="Student not found")
#     # db.delete(db_student)
#     db_student.delete(synchronize_session=False)

#     db.commit()
#     return {"message": "Student deleted successfully"}

# # if __name__ == "__main__":
# #     models.Base.metadata.create_all(bind=database.engine)


# @app.post("/create_user/",status_code=status.HTTP_201_CREATED,response_model=ShowUserSchema,tags=["USER"])
# def create_user(request:UserSchema,db:Session = Depends(get_db)):
#     createuser = UserModel(name = request.name,email=request.email,password = Hash.get_password_hash(request.password))
#     db.add(createuser)
#     db.commit()
#     db.refresh(createuser)
#     return createuser


# @app.get("/user/{id}",response_model=ShowUserSchema,tags=["USER"])
# def get_user(id:int,db:Session=Depends(get_db)):
#     user = db.query(UserModel).filter(UserModel.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No user present with id={id}")
#     return user

# @app.get("/user/",response_model=List[ShowUserSchema],tags=["USER"])
# def get_users(db:Session=Depends(get_db)):
#     user = db.query(UserModel).all()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No user present")
#     return user
