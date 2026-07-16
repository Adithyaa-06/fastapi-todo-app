from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI()
class Task(BaseModel):
    id: int
    title: str
    done: bool
class TaskCreate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

tasks = [
    {"id": 1, "title": "Task 1", "done": False},
    {"id": 2, "title": "Task 2", "done": True},
    {"id": 3, "title": "Task 3", "done": False},
]
@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.post("/tasks")
async def create_task(task: TaskCreate):
    if not task.title or not task.title.strip():
        return JSONResponse(status_code=400, content={"error": "Task title is missing"})
    next_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)
    return JSONResponse(status_code=201, content=new_task)

def find_task(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    return None
@app.put("/tasks/{id}")
async def update_task(id:int, task: TaskCreate):
    t = find_task(id)
    if not t:
        return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
    if task.title is None and task.done is None:
        return JSONResponse(status_code=400, content={"error": "Need fields to update"})
    if task.title is not None:
        t["title"] = task.title
    if task.done is not None:
        t["done"] = task.done
    return JSONResponse(status_code=200, content=t)             