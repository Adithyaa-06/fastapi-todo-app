# FastAPI To-Do CRUD API

A to-do list API built with FastAPI, supporting full CRUD operations (create, read, update, delete) on tasks. Data is stored in memory — no database required.

## Setup & Run

```bash
git clone https://github.com/Adithyaa-06/fastapi-todo-app.git
cd fastapi-todo-app
uv venv
.venv\Scripts\activate    # Windows (adjust if using a different shell)
uv pip install -r requirements.txt
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`. Interactive docs available at `http://localhost:8000/docs`.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Returns API info |
| GET | /health | Returns health status |
| GET | /tasks | Returns all tasks |
| POST | /tasks | Creates a new task |
| GET | /tasks/{id} | Returns a task by ID |
| PUT | /tasks/{id} | Updates a task by ID |
| DELETE | /tasks/{id} | Deletes a task by ID |

## Example Request

```
curl -i http://localhost:8000/tasks
```

```
HTTP/1.1 200 OK
date: Thu, 16 Jul 2026 13:35:33 GMT
server: uvicorn
content-length: 79
content-type: application/json

[{"id":1,"title":"Task 1","done":false},{"id":3,"title":"Task 3","done":false}]
```

## Design Notes

A few deliberate decisions worth calling out, since the "right" answer wasn't always the obvious one:

- **Separate input models for create vs update.** Pydantic makes all declared fields required by default, but the assignment's spec needs `POST` with a missing title to return `400` (not FastAPI's default `422`), and `PUT` needs to support partial updates (title and/or done). Both required loosening the model — fields typed as `Optional` with `None` defaults — and moving the actual validation into the route logic instead of relying on Pydantic's automatic schema check. Tradeoff: the model itself no longer documents "title is required" at a glance; that responsibility now lives in the function body.
- **`None` vs `False` as a default matters.** The update model originally defaulted `done` to `False`, which meant an empty `PUT` body could silently overwrite a task's real `done` state back to `false` — data corruption disguised as a no-op request. Defaulting to `None` instead of `False` lets the code distinguish "the client didn't send this field" from "the client explicitly set it to false."
- **`Response` vs `JSONResponse` for 204.** A `DELETE` returning `204 No Content` can't carry a body at all — that's part of the HTTP spec, not a style choice. `JSONResponse` always tries to serialize *something*, even `None`, which breaks a 204. Plain `Response(status_code=204)` sends nothing, matching what 204 actually means.
- **Shared `find_task` helper instead of duplicating the lookup.** `GET`, `PUT`, and `DELETE` all need to locate a task by id and 404 if it's missing. Writing that loop three times would mean three places to update if the storage structure ever changes (e.g. moving from a list to a dict).

## Swagger UI

All endpoints tested via Swagger's "Try it out" — full CRUD cycle confirmed (create, read, update, delete).

![Swagger UI](Photos)