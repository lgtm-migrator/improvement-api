from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import settings
from app.main import app


client = TestClient(app)


test_user = {"username": "testuser", "password": "verystrongpassword"}
access_res_dict = {"access_token": 1, "token_type": 2}


def test_should_register_a_new_user_and_return_token():
    response = client.post("/api/auth/register", data=test_user)
    assert response.status_code == 200

    data = response.json()

    assert access_res_dict.keys() >= {"access_token", "token_type"}

    token = data.get("access_token")
    payload_sub = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]).get("sub")

    assert payload_sub.find(test_user.get("username")) != -1


def test_register_should_fail_with_existing_username():
    response = client.post("/api/auth/register", data=test_user)
    assert response.status_code == 400

    data = response.json()

    assert data.get("detail") == "This username is already taken."


def test_should_create_access_token():
    response = client.post("/api/auth/access-token", data=test_user)
    assert response.status_code == 200

    data = response.json()

    assert access_res_dict.keys() >= {"access_token", "token_type"}

    token = data.get("access_token")
    payload_sub = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]).get("sub")

    assert payload_sub.find(test_user.get("username")) != -1
