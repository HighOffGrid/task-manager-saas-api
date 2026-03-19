from unittest.mock import Mock, patch
from fastapi import HTTPException

from app.services.task_service import create_task_service


def test_create_task_service_success():
    db = Mock()
    data = Mock()
    data.project_id = 1
    data.model_dump.return_value = {
        "title": "Nova tarefa",
        "description": "Descricao teste",
        "project_id": 1
    }

    fake_project = Mock()
    fake_created_task = Mock()
    fake_created_task.id = 10

    db.query.return_value.filter.return_value.first.return_value = fake_project

    with patch("app.services.task_service.Task") as mock_task, \
         patch("app.services.task_service.task_repo.create_task", return_value=fake_created_task):

        result = create_task_service(db, data)

        mock_task.assert_called_once_with(**data.model_dump.return_value)
        assert result == fake_created_task
        assert result.id == 10


def test_create_task_service_project_not_found():
    db = Mock()
    data = Mock()
    data.project_id = 999

    db.query.return_value.filter.return_value.first.return_value = None

    try:
        create_task_service(db, data)
        assert False, "Expected HTTPException to be raised"
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Project not found"


def test_create_task_service_internal_error():
    db = Mock()
    data = Mock()
    data.project_id = 1

    db.query.side_effect = Exception("Database failure")

    try:
        create_task_service(db, data)
        assert False, "Expected HTTPException to be raised"
    except HTTPException as exc:
        assert exc.status_code == 500
        assert exc.detail == "Internal server error"