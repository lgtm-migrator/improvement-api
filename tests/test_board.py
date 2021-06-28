from typing import Any
from typing import Optional

from fastapi.testclient import TestClient
from requests.structures import CaseInsensitiveDict  # type: ignore

from app.main import app


client = TestClient(app)


def create_headers(user_in_db):
    response = client.post("/api/auth/access-token", data=user_in_db)

    data = response.json()
    token = data.get("accessToken")

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"

    return headers


headers = create_headers({"username": "testuser_exists", "password": "superstrongpassword"})


def create_three_new_boards():
    new_boards = []

    for i in range(1, 4):
        new_boards.append({"board_name": f"test board {i}", "owner_uuid": "1088292a-46cc-4258-85b6-9611f09e1830"})

    return new_boards


def test_should_create_new_boards():
    new_boards = create_three_new_boards()

    for i, new_board in enumerate(new_boards):
        response = client.post("/api/board/create", json=new_board, headers=headers)
        assert response.status_code == 200

        data = response.json()
        assert data.get("boardName") == f"test board {i+1}"


def test_should_get_user_boards():
    # Fetch multiple boards
    response = client.get(
        "/api/board/list", params={"user_uuid": "1088292a-46cc-4258-85b6-9611f09e1830"}, headers=headers
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3

    for board in data:
        assert board.get("ownerUuid") == "1088292a-46cc-4258-85b6-9611f09e1830"

    first_board_uuid = data[0].get("boardUuid")

    # Fetch one board
    response = client.get(
        f"/api/board/list/{first_board_uuid}",
        params={"userUuid": "1088292a-46cc-4258-85b6-9611f09e1830"},
        headers=headers,
    )
    assert response.status_code == 200


def test_should_update_user_board():
    response = client.get(
        "/api/board/list", params={"userUuid": "1088292a-46cc-4258-85b6-9611f09e1830"}, headers=headers
    )
    data = response.json()

    updated_board = {
        "boardUuid": data[0].get("boardUuid"),  # just use some uuid from the first response
        "boardName": "test board booyaa",
        "ownerUuid": "1088292a-46cc-4258-85b6-9611f09e1830",
    }

    response = client.put(
        "/api/board/update",
        params={"user_uuid": "1088292a-46cc-4258-85b6-9611f09e1830"},
        json=updated_board,
        headers=headers,
    )
    assert response.status_code == 200

    data = response.json()

    assert data.get("boardName") == "test board booyaa"


def test_should_delete_user_board():
    response = client.get(
        "/api/board/list", params={"user_uuid": "1088292a-46cc-4258-85b6-9611f09e1830"}, headers=headers
    )
    board_uuid = response.json()[0].get("boardUuid")

    response = client.delete(
        "/api/board/delete",
        params={"user_uuid": "1088292a-46cc-4258-85b6-9611f09e1830", "board_uuid": board_uuid},
        headers=headers,
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 0

    # check that the board isn't found anymore
    response = client.get(
        f"/api/board/list/{board_uuid}", params={"userUuid": "1088292a-46cc-4258-85b6-9611f09e1830"}, headers=headers
    )
    assert response.status_code == 404
