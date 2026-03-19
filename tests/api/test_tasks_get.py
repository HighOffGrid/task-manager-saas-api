from unittest.mock import patch
from app.main import app
from app.core.dependencies import get_current_user
from fastapi import HTTPException


def override_get_current_user():
    class User:
        id = 1
        email = "teste@teste.com"
    return User()


def test_get_all_tasks_route_success(client):
    app.dependency_overrides[get_current_user] = override_get_current_user

    fake_page = [
        {
            "id": 1,
            "title": "Task 1",
            "description": "Descricao 1",
            "status": "pending",
            "project_id": 1,
            "created_at": None,
            "updated_at": None
        },
        {
            "id": 2,
            "title": "Task 2",
            "description": "Descricao 2",
            "status": "done",
            "project_id": 1,
            "created_at": None,
            "updated_at": None
        }
    ]

    with patch(
        "app.api.routes.task_routes.task_service.get_all_tasks_service",
          return_value=fake_page,
    ):
        response = client.get("/tasks/")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert len(body["items"]) == 2
    assert body["items"][0]["title"] == "Task 1"


def test_get_task_by_id_route_success(client):
    app.dependency_overrides[get_current_user] = override_get_current_user

    task_id = 1
    fake_page = {
        "id": task_id,
        "title": "Task 1",
        "description": "Descricao 1",
        "status": "pending",
        "project_id": 1,
        "created_at": None,
        "updated_at": None
    }

    with patch(
        "app.api.routes.task_routes.task_service.get_task_by_id_service",
        return_value=fake_page,
    ):
        response = client.get(f"/tasks/{task_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Task 1"


def test_get_task_by_id_route_not_found(client):
    app.dependency_overrides[get_current_user] = override_get_current_user

    task_id = 999

    with patch(
        "app.api.routes.task_routes.task_service.get_task_by_id_service",
        side_effect=HTTPException(status_code=404, detail="Task not found"),
    ):
        response = client.get(f"/tasks/{task_id}")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
