from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoint": ["/tasks"]}

@app.get("/health")
async def health():
    return {"status": "ok"}
