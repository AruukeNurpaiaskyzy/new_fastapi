import strawberry
from typing import List, Optional, Dict, Any
from strawberry.fastapi import GraphQLRouter
from datetime import datetime
tasks_db = []
users_db = []
current_task_id = 1
current_user_id = 1


@strawberry.type
class Task:
    """the types of the tasks"""
    id: int
    title: str
    description: str
    completed: bool
    user_id: int
    created_at: str

@strawberry.type 