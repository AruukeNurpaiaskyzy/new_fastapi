from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional


router = APIRouter(prefix="/users", tags=['users'])

class UserResponse(BaseModel):
    id:int
    username:str
    email: str

users_db = [
    {"id": 1, "username": "alex", "email": "alex@example.com"},
    {"id": 2, "username": "maria", "email": "maria@example.com"},

]

@router.get("/", response_model=List[UserResponse])
def get_users():
    return users_db

@router.get("/{user_id}", response_model=UserResponse)
def get_user (user_id:int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="the user is not found")