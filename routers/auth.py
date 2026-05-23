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

@router.post("/login",  response_model=LoginResponse)
def login (credentials: LoginRequest):
    user = fake_users.get(credentials.email)
    if not user or user ["password"] != credentials.password:
        raise HTTPException(status_code=401, detail= "wrong password")
    
    fake_token = f"fake_token_{credentials.email}_{datetime.now()}"

    return {
        "access_token": fake_token,
        "token_type": "bearer",
        "message": f"Welcome, {user['username']}!"
    }

class RegisterRequest(BaseModel):
    username:str
    email: str
    password:str

@router.post("/register")
def register(user_date: RegisterRequest):
    if user_data.email in fake_users:
        raise HTTPException(status_code=400, detail="The user is already exists")
    fake_users[user_data.email] = {
        "password": user_data.password,
        "username": user_data.username
    }

    return {"message": " the registration has done successfully! you can login"}