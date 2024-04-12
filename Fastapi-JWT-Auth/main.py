from fastapi import FastAPI,status,HTTPException,Depends
from typing import List
import schemas
from fastapi_jwt_auth import AuthJWT
import math

@AuthJWT.load_config
def get_config():
    return schemas.Settings()


app = FastAPI()

users=[]

@app.get("/")
def index():
    return {"msg":" testing Api"}

@app.post('/signup',status_code=201)
def create_user(user:schemas.User):
    new_user = {
        "username":user.username,
        "email":user.email,
        "password":user.password
    }

    users.append(new_user)
    return new_user

@app.get('/users',response_model=List[schemas.User])
def get_users():
    return users

    

@app.post('/login')
def login(user: schemas.UserLogin, Authorize: AuthJWT = Depends()):
    # if user.username != "test" or user.password != "test":
    for u in users:
        if (u['username']==user.username) and (u['password']==user.password):
            access_token = Authorize.create_access_token(subject=user.username)
            refresh_token = Authorize.create_refresh_token(subject=user.username)
            return {"access_token": access_token,"refresh_token":refresh_token}
    raise HTTPException(status_code=401,detail="Invalid username or password")
    

@app.get('/protected')
def get_logged_in_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")    
    current_user = Authorize.get_jwt_subject()
    return {"c_user": current_user}

@app.get("/refresh_token")
def create_refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return {"new_access_token":access_token }

@app.post('/fresh_login')
def fresh_login(user:schemas.UserLogin,Authorize:AuthJWT=Depends()):
    for u in users:
        if (u['username']==user.username) and (u['password']==user.password):

            fresh_token = Authorize.create_access_token(subject=user.username,fresh=True)
            return {"fresh_token": fresh_token}
        
    raise HTTPException(status_code=401,detail="Invalid username or password")

@app.get('/fresh_url')
def get_user(Authorize:AuthJWT=Depends()):
    try:
        Authorize.fresh_jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invaild token")
    
    current_user = Authorize.get_jwt_subject()
    return current_user                                



@app.get('/items')
def items(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invaild token")
    

    items = [
        "item1",
        "item2",
        "item3"
    ]

    return {"items": items}