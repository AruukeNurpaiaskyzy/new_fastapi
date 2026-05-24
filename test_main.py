from fastapi.testclient import TestClient
from main import app
import  pytest

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "endpoints" in response.json()

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_create_task():
    task_data = {"title": "testing task", "description": "this is a test"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    assert response.json()["message"] == "the task is created"

def test_get_users():
    response  = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_auth_login_success():
    credentials = {"email": "user@example.com", "password": "password123"}
    response = client.post("/auth/login", json=credentials)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_auth_login_fail():
    credentials = {"email": "wrong@example.com", "password": "wrong"}
    response = client.post("/auth/login", json=credentials)
    assert response.status_code == 401

def test_register():
    user_data = {
        "username": "newuser",
        "email": "new@example.com", 
        "password": "newpass123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert "the registration has successfully done" in response.json()["message"]