from fastapi.testclient import TestClient
from main import app
import requests
import schemas
from jose import jwt
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# client = TestClient(app)

url_1 = "http://127.0.0.1:8000/User"
url_2 = "http://127.0.0.1:8000/Task"
LOGIN_URL = "http://127.0.0.1:8000/login/"

def test_create_user():
        url = url_1+'/create_user/'
        print(url)
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

        data={
  "username": "pratikc",
  "password": "pratikc",
  "email": "pratik"
}
        response = requests.request("post", url, headers=headers,json=data)
        # print(**response.json())
        # response_jsondata = response.json()

        sc= schemas.ShowUser(**response.json())
        assert sc.username == "pratikc"
        # assert response.json()
        assert response.status_code == 201
        # assert response_jsondata.username == "pratik12" 

        # assert response_jsondata. == 201
        # assert response_jsondata['status'] == "success"
        # print(response_jsondata['status'])
        return sc


def test_login_user(LOGIN_URL,test_user):
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

        data = {
                "username" : "pass",
                "password": "pass"
        }
        res = requests.request("post",url=LOGIN_URL,headers=headers,json=data)

        login_res = 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
