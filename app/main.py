
import os
import uuid
from pathlib import Path

import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="TaskTrack Team")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
STATIC_DIR = Path(__file__).resolve().parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def get_redis():
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class Task(BaseModel):
    id: str
    title: str
    completed: bool = False


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    try:
        get_redis().ping()
        return {"status": "healthy"}
    except redis.RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    new_task = Task(
        id=str(uuid.uuid4()),
        title=task.title,
        completed=False
    )

    get_redis().hset(
        "tasktrack:tasks",
        new_task.id,
        new_task.model_dump_json()
    )

    return new_task


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    values = get_redis().hvals("tasktrack:tasks")
    tasks = [Task.model_validate_json(value) for value in values]
    return sorted(tasks, key=lambda task: task.title)


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: str):
    client = get_redis()
    stored = client.hget("tasktrack:tasks", task_id)

    if stored is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task = Task.model_validate_json(stored)
    task.completed = True

    client.hset(
        "tasktrack:tasks",
        task_id,
        task.model_dump_json()
    )

    return task
