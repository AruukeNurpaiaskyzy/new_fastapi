from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter (prefix="/auth", tags = ['auth'])

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    message: str


fake_users = {
    "user@example.com": {
        "password": "password123",
        "username": "testuser"
    }
}

