from uuid import uuid4

from fastapi.testclient import TestClient
from requests.structures import CaseInsensitiveDict  # type: ignore

from .conftest import test_user_in_db
from .conftest import TEST_USER_IN_DB_PASSWORD


def create_headers(user_in_db, test_client: TestClient):
    response = test_client.post("/api/auth/access-token", data=user_in_db)

    data = response.json()
    token = data.get("accessToken")

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"

    return headers


headers_user_data = {"username": test_user_in_db.get("username"), "password": TEST_USER_IN_DB_PASSWORD}


def create_three_new_boards():
    new_boards = []

    for i in range(1, 4):
        new_boards.append({"boardName": f"test board {i}", "ownerUuid": test_user_in_db.get("user_uuid")})

    return new_boards


def test_should_create_new_boards(test_client: TestClient):
    new_boards = create_three_new_boards()

    for i, new_board in enumerate(new_boards):
        response = test_client.post(
            "/api/board/create", json=new_board, headers=create_headers(headers_user_data, test_client)
        )
        assert response.status_code == 200

        data = response.json()
        assert data.get("boardName") == f"test board {i+1}"


def test_should_get_user_boards(test_client: TestClient):
    # Fetch multiple boards
    response = test_client.get("/api/board/list", headers=create_headers(headers_user_data, test_client))
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 4  # three created during tests +1 during test db init

    for board in data:
        assert board.get("ownerUuid") == test_user_in_db.get("user_uuid")

    first_board_uuid = data[0].get("boardUuid")

    # Fetch one board
    response = test_client.get(
        f"/api/board/list/{first_board_uuid}",
        headers=create_headers(headers_user_data, test_client),
    )
    assert response.status_code == 200


def test_should_update_user_board(test_client: TestClient):
    response = test_client.get("/api/board/list", headers=create_headers(headers_user_data, test_client))
    data = response.json()

    updated_board = {
        "boardUuid": data[0].get("boardUuid"),  # just use some uuid from the first response
        "boardName": "test board booyaa",
        "ownerUuid": test_user_in_db.get("user_uuid"),
        "columnOrder": [str(uuid4()), str(uuid4()), str(uuid4())],
    }

    response = test_client.put(
        "/api/board/update",
        json=updated_board,
        headers=create_headers(headers_user_data, test_client),
    )
    assert response.status_code == 200

    data = response.json()

    assert data.get("boardName") == "test board booyaa"
    assert len(data.get("columnOrder")) == 3


def test_should_delete_user_board(test_client: TestClient):
    response = test_client.get("/api/board/list", headers=create_headers(headers_user_data, test_client))
    board_uuid = response.json()[0].get("boardUuid")

    response = test_client.delete(
        f"/api/board/delete/{board_uuid}",
        headers=create_headers(headers_user_data, test_client),
    )
    assert response.status_code == 200

    data = response.json()
    assert data[0].get("delete_board") is None  # noqa: E711

    # check that the board isn't found anymore
    response = test_client.get(f"/api/board/list/{board_uuid}", headers=create_headers(headers_user_data, test_client))
    assert response.status_code == 404
