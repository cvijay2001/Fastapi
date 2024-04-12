from fastapi.testclient import TestClient
from main import app
import requests
import schemas
# client = TestClient(app)

url_1 = "http://127.0.0.1:8000/User"
url_2 = "http://127.0.0.1:8000/Task"

# def test_create_user():
  
#     res = client.post("http://127.0.0.1:8000/User/create_user/",json={"username": "vi123","password": "vi123","email": "vij123"})
#     new_user = schemas.ShowUser(**res.json())

#     assert new_user.email == "vij123"

# def test_login_user():
#     res = client.post("/login/",json={"username": "regular","password": "regular"})
    
#     assert res.status_code == 201




def test_get_cost_summary():
        url = url_1+'/create_user/'
        print(url)
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }

        data={
  "username": "pratik",
  "password": "pratik",
  "email": "pratik"
}

        response = requests.request("post", url, headers=headers,data=data)
        print(response)
        response_jsondata = response.json()

        # assert response_jsondata. == 201
        assert response_jsondata['status'] == "success"
        print(response_jsondata['status'])