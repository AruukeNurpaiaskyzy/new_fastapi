from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
router = APIRouter(prefix="/tasks", tags=['tasks'])

class TaskCreate(BaseModel):
    title:str
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id:int
    title:str
    description:str
    completed:bool

@router.get("/")
def get_tasks():
    return[{"id": 1, "title": "Learn FastAPI"}]
