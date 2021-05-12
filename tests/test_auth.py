from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_should_register_a_new_user_with_token():
    response = client.post("/api/users/register", json={"username": "testihenri", "password": "vahvasalasana"})
    assert response.status_code == 200

    data = response.json()

    user_res_dict = {"user_uid": 1, "username": 2, "token_data": 3}

    assert user_res_dict.keys() >= {"user_uid", "username", "token_data"}

    assert data.get("username") == "testihenri"


def test_register_should_fail_with_existing_username():
    response = client.post("/api/users/register", json={"username": "testihenri", "password": "vahvasalasana"})
    assert response.status_code == 400

    data = response.json()

    assert data.get("detail") == "This username is already taken."
