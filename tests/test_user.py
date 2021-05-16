from fastapi.testclient import TestClient
from requests.structures import CaseInsensitiveDict

from app.main import app
from app.models.user import UserDBBase


client = TestClient(app)


user_data_keys = UserDBBase.schema().get("properties").keys()


def test_should_return_user_data(user_in_db):
    response = client.post("/api/auth/access-token", data=user_in_db)
    assert response.status_code == 200

    data = response.json()
    token = data.get("access_token")

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"

    response = client.get("/api/user/me", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert user_data_keys == data.keys()
    assert user_in_db.get("username") == data.get("username")
