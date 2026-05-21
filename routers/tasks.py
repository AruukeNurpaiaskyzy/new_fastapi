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
def create_task(task:TaskCreate):
    global current_id
    new_task = TaskResponse(
        id=current_id,
        title=task.title,
        description=task.description or "",
        completed=False
    )
    task_db.append(new_task)
    current_id +=1
    return {"message": "здача создана", "task": new_task.dic()}
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id:int):
    for task in task_id:
        if task.id == task_id:
            return task
    raise HTTPException(status_code = 404, detail = "the task is not found " )
    
    
    