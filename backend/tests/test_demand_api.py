from fastapi.testclient import TestClient
import pytest
from ..main import app, session
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..api.client import get_session

@pytest.mark.order(11)
def test_post_demand(client):
    response = client.post(
        "/api/demands/",
        json={
            "team_id": 1,
            "epic_id": 1,
            "year": 2022,
            "month": 3,
            "days": 18,
            "created_at": "2022-03-15T13:46:24.344Z",
            "updated_at": "2022-03-15T13:46:24.344Z",
            "is_locked": False,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data == {
        "id": 1,
        "team_id": 1,
        "epic_id": 1,
        "year": 2022,
        "month": 3,
        "days": 18,
        "created_at": "2022-03-15T13:46:24.344000",
        "updated_at": "2022-03-15T13:46:24.344000",
        "is_locked": False,
    }


def test_get_demands(client):
    response = client.get("/api/demands/")
    data = response.json()
    assert data == [
        {
            "id": 1,
            "team_id": 1,
            "epic_id": 1,
            "year": 2022,
            "month": 3,
            "days": 18,
            "created_at": "2022-03-15T13:46:24.344000",
            "updated_at": "2022-03-15T13:46:24.344000",
            "is_locked": False,
        }
    ]


def test_delete_demand(client):
    response = client.delete("/api/demands/?demand_id=1")
    assert response.status_code == 200
