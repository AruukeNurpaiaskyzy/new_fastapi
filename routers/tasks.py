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
task_db = []
current_id = 1

@router.get("/", response_model=List[TaskResponse])
def get_tasks():
    return task_db

@router.post("/", response_model=dict)


