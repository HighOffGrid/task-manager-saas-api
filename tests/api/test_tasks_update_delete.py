from unittest.mock import patch
from fastapi import HTTPException


def test_update_task_route_success(client):
    task_id = 1
    payload = {
        "title": "Tarefa atualizada",
        "description": "Descricao atualizada",
        "status": "in_progress",
        "project_id": 1
    }

    updated_task = {
        "id": task_id,
        "title": "Tarefa atualizada",
        "description": "Descricao atualizada",
        "status": "in_progress",
        "project_id": 1,
        "created_at": None,
        "updated_at": None
    }

    with patch(
        "app.api.routes.task_routes.task_service.update_task_service",
        return_value=updated_task
    ):
        response = client.put(f"/tasks/{task_id}", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == task_id
    assert body["title"] == "Tarefa atualizada"
    assert body["status"] == "in_progress"


def test_update_task_route_not_found(client):
    task_id = 999
    payload = {
        "title": "Tarefa atualizada",
        "description": "Descricao atualizada",
        "status": "in_progress",
        "project_id": 1
    }

    with patch(
        "app.api.routes.task_routes.task_service.update_task_service",
        side_effect=HTTPException(status_code=404, detail="Task not found")
    ):
        response = client.put(f"/tasks/{task_id}", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_route_invalid_field_type(client):
    task_id = 1
    payload = {
        "title": 123,
        "description": "Descricao atualizada",
        "status": "in_progress",
        "project_id": 1
    }

    response = client.put(f"/tasks/{task_id}", json=payload)

    assert response.status_code == 422


def test_delete_task_route_success(client):
    task_id = 1

    with patch(
        "app.api.routes.task_routes.task_service.delete_task_service",
        return_value={"message": "Task deleted successfully"}
    ):
        response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


def test_delete_task_route_not_found(client):
    task_id = 999

    with patch(
        "app.api.routes.task_routes.task_service.delete_task_service",
        side_effect=HTTPException(status_code=404, detail="Task not found")
    ):
        response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"