from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
