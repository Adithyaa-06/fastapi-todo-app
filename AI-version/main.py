from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str

class TaskCreate(BaseModel):
    title: str

tasks = []
next_id = 1

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": task.title}
    tasks.append(new_task)
    next_id += 1
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate):
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = task.title
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")