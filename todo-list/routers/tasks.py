from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from models import Task
from database import get_connection

router = APIRouter()


@router.post("/tasks", response_model=Task)
async def create_task(task: Task):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO tasks (title, description, status, priority, created_at) VALUES (%s, %s, %s, %s, NOW())",
            (task.title, task.description, task.status, task.priority)
        )
        task.id = cursor.lastrowid
    conn.close()
    return task


@router.get("/tasks", response_model=list[Task])
async def get_tasks(
    status: Optional[str] = None,
    priority: Optional[int] = None,
    sort_by_date: Optional[bool] = False
):
    conn = await get_connection()
    query = "SELECT id, title, description, status, priority, created_at FROM tasks WHERE 1=1"
    params = []
    if status:
        query += " AND status = %s"
        params.append(status)
    if priority:
        query += " AND priority = %s"
        params.append(priority)
    if sort_by_date:
        query += " ORDER BY created_at DESC"
    async with conn.cursor() as cursor:
        await cursor.execute(query, params)
        rows = await cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
    conn.close()
    return [
        Task(**{**dict(zip(column_names, row)),
             "created_at": row[-1].isoformat()})
        for row in rows
    ]


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute(
            "UPDATE tasks SET title = %s, description = %s, status = %s, priority = %s WHERE id = %s",
            (task.title, task.description, task.status, task.priority, task_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
    conn.close()
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
    conn.close()
    return {"detail": "Task deleted"}
