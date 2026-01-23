from fastapi import FastAPI
from backend.db import create_db_and_tables

app = FastAPI(title="Todo App API", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Todo App API"}

# Import and include routes
from backend.routes import tasks
app.include_router(tasks.router, prefix="/api")