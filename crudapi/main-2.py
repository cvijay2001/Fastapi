from typing import Union
from schemas import Student
from fastapi import FastAPI,Depends

import models,database
from sqlalchemy.orm import Session

# from fastapi.responses import RedirectResponse

# app = FastAPI()

# @app.get("/")
# def redirect_to_google():
#     return RedirectResponse(url="https://www.google.com")

app = FastAPI()

get_db = database.get_db
models.Base.metadata.create_all(database.engine)

def create(request: Student,db:Session):
    new_user = models.StudentModel(name=request.name,age=request.age,city=request.city)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.post("/Student/")
# def add_student(student: Student,db: Session = Depends(get_db)):
#     return create(Student,db)

@app.post("/Student/")
def add_student(student: Student, db: Session = Depends(get_db)):
    return create(student, db)
