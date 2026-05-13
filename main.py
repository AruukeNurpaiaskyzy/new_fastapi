# from fastapi import FastAPI
# app = FastAPI()
# @app.get('/')
# def root():
#     return {'message': 'Hello FastAPI'}

from pydantic import BaseModel
from typing import List
from routers import tasks
app.include_router(tasks.riuter)


class Task(BaseModel):
    id: int
    title: str
    completed: bool=False

task_db = []
@app.post("tasks/", response_model = Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task
@app.get("tasks/", response_model=List(Task))
def get_task():
    return tasks_db