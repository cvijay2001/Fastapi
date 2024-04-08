from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
import schemas
import database
from repository import authentication
from hashing import Hash
import JWTtoken 
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from blog.repository import blog

router = APIRouter(
    # prefix="/accounts",
    tags=['authentication']
)

get_db = database.get_db


@router.post("/login/",status_code=status.HTTP_201_CREATED)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):

# def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    print(form_data)
    print(" Entered login api")

    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    print("user----->",user)
    print("type",type(user))
    if not user:
        print(" i am in not user")
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="wrong credentials")
    
    if not Hash.verify_password(form_data.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Password")
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )\

    access_token = JWTtoken.create_access_token(
        data={"sub": user.email})
    
    print("print access_token generated: ", access_token)
    return schemas.Token(access_token=access_token, token_type="bearer")
        

    # return "login"