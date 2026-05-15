from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code ==200
    

def test_root_endpoint():
    """Тест корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_tasks():
    """Тест получения списка задач"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert "tasks" in response.json()

def test_create_task():
    """Тест создания задачи"""
    task_data = {"title": "Тестовая задача", "description": "Это тест"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Задача создана"

def test_get_users():
    """Тест получения списка пользователей"""
    response = client.get("/users")
    assert response.status_code == 200
    assert "users" in response.json()

def test_auth_login():
    """Тест авторизации"""
    credentials = {"email": "user@example.com", "password": "password123"}
    response = client.post("/auth/login", json=credentials)
    assert response.status_code == 200