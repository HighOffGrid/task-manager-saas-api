from unittest.mock import patch
from fastapi import HTTPException


def test_create_task_route_success(client):
    payload = {
        "title": "Nova tarefa",
        "description": "Descricao teste",
        "status": "pending",
        "project_id": 1
    }

    fake_task = {
        "id": 10,
        "title": "Nova tarefa",
        "description": "Descricao teste",
        "status": "pending",
        "project_id": 1,
        "created_at": None,
        "updated_at": None
    }

    with patch(
        "app.api.routes.task_routes.task_service.create_task_service",
        return_value=fake_task
    ):
        response = client.post("/tasks/", json=payload)

    assert response.status_code in [200, 201]
    body = response.json()
    assert body["id"] == 10
    assert body["title"] == "Nova tarefa"


def test_create_task_route_project_not_found(client):
    payload = {
        "title": "Nova tarefa",
        "description": "Descricao teste",
        "status": "pending",
        "project_id": 999
    }

    with patch(
        "app.api.routes.task_routes.task_service.create_task_service",
        side_effect=HTTPException(status_code=404, detail="Project not found")
    ):
        response = client.post("/tasks/", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_task_route_invalid_payload(client):
    response = client.post("/tasks/", json={})
    assert response.status_code == 422