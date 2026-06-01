from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from celery.result import AsyncResult

# Импортируем наши Celery задачи
from celery_tasks import say_hello, process_data, send_email, async_http_call
from celery_app import celery_app

router = APIRouter(prefix="/tasks", tags=['tasks'])

# Модели данных
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

class HelloTaskRequest(BaseModel):
    name: str
    delay_seconds: int = 5

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str

# ===== ОБЫЧНЫЕ ЗАДАЧИ (как было раньше) =====
tasks_db = []
current_id = 1

@router.get("/", response_model=List[TaskResponse])
def get_tasks():
    return tasks_db

@router.post("/", response_model=dict)
def create_task(task: TaskCreate):
    global current_id
    new_task = TaskResponse(
        id=current_id,
        title=task.title,
        description=task.description or "",
        completed=False
    )
    tasks_db.append(new_task)
    current_id += 1
    return {"message": "Задача создана", "task": new_task.dict()}

@router.delete("/{task_id}")
def delete_task(task_id: int):
    global tasks_db
    for i, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(i)
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")

# ===== НОВЫЕ: ФОНОВЫЕ ЗАДАЧИ C CELERY =====

# 1. Запустить фоновую задачу (приветствие с задержкой)
@router.post("/celery/hello")
def start_hello_task(request: HelloTaskRequest):
    """
    Запускает фоновую задачу, которая выполнится через delay_seconds секунд
    """
    task = say_hello.delay(request.name, request.delay_seconds)
    return {
        "task_id": task.id,
        "status": "Задача запущена",
        "message": f"Через {request.delay_seconds} секунд {request.name} получит приветствие"
    }

# 2. Проверить статус задачи
@router.get("/celery/{task_id}/status")
def get_task_status(task_id: str):
    """
    Проверяет статус фоновой задачи
    """
    task_result = AsyncResult(task_id, app=celery_app)
    
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "ready": task_result.ready(),
    }
    
    if task_result.ready():
        if task_result.successful():
            result["result"] = task_result.result
        else:
            result["error"] = str(task_result.info)
    
    # Если задача в процессе, показываем прогресс
    if task_result.state == "PROGRESS":
        result["progress"] = task_result.info.get("progress", 0)
        result["current"] = task_result.info.get("current", 0)
        result["total"] = task_result.info.get("total", 0)
    
    return result

# 3. Запустить задачу с прогрессом
@router.post("/celery/process/{count}")
def start_process_task(count: int):
    """
    Запускает задачу, которая обрабатывает count элементов с показом прогресса
    """
    task = process_data.delay(count)
    return {
        "task_id": task.id,
        "status": "Обработка запущена",
        "total_items": count,
        "check_url": f"/tasks/celery/{task.id}/status"
    }

# 4. Отправить email в фоне
@router.post("/celery/send-email")
def start_email_task(email_request: EmailRequest):
    """
    Отправляет email в фоновом режиме
    """
    task = send_email.delay(
        email_request.to_email,
        email_request.subject,
        email_request.body
    )
    return {
        "task_id": task.id,
        "status": "Письмо отправляется в фоне",
        "to": email_request.to_email
    }

# 5. Сделать HTTP запрос в фоне
@router.post("/celery/fetch-url")
def start_fetch_task(url: str):
    """
    Делает HTTP запрос к указанному URL в фоновом режиме
    """
    task = async_http_call.delay(url)
    return {
        "task_id": task.id,
        "status": "Запрос выполняется",
        "url": url
    }

# 6. Отменить задачу (если еще не началась)
@router.delete("/celery/{task_id}/cancel")
def cancel_task(task_id: str):
    """
    Отменяет задачу (только если она еще не начала выполняться)
    """
    celery_app.control.revoke(task_id, terminate=False)
    return {"message": f"Задача {task_id} отменена"}

# 7. Получить все активные задачи (админская фича)
@router.get("/celery/active")
def get_active_tasks():
    """
    Показывает все активные задачи (для отладки)
    """
    inspect = celery_app.control.inspect()
    active = inspect.active()
    scheduled = inspect.scheduled()
    reserved = inspect.reserved()
    
    return {
        "active": active or {},
        "scheduled": scheduled or {},
        "reserved": reserved or {}
    }