from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import schemas,models
from sqlalchemy.orm import Session

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str,credentials_exception,db:Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print("username---------------->",username)
        # email : str = payload.get("sub")
        if username is None:
            raise credentials_exception     
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    c_user= db.query(models.User).filter(models.User.username==token_data.username).first()

    return c_user

    
    # c_user = get_user(fake_users_db, username=token_data.username)

    # if c_user is None:
    #     raise credentials_exception
    # return c_user


