from pydantic import BaseModel

class User(BaseModel):
    username:str
    email:str
    password:str

    # schema_extra = {
    #     "example":{
    #         "username":"john doe",
    #         "email":"email",
    #         "password":"password"
    # }
    #         }
    


class Settings(BaseModel):
    authjwt_secret_key: str = "9eb622ca6d551871ac3ce69ad67b344320f74f615f0d3e9d1613ff321faa7f75"


class UserLogin(BaseModel):
    username:str
    password:str
    # schema_extra = {
    #     "example":{
    #         "username":"john doe",
    #         "password":"password"
    #     }
    # }