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
    
@router.delete("/{task_id}")
def delete_task(task_id: int):
    global tasks_db
    for i, task in enumerate(tasks_db):
        if task.id==task_id:
           tasks_db.pop(i)
        return {"message": "the task is deleted"}
    raise HTTPException(status_code=404, detail="the task is not found")

@router.put("/{task_id}")
def update_task(task_id:int, task_update: TaskCreate):
    for task in tasks_db:
        if task.id == task_id:
            task.title = task_update.title
            task.description = task_update.description or ""
            return {"message": "the task is updated", "task": task.dict()}
    raise HTTPException(status_code=404, detail="the task is not found")