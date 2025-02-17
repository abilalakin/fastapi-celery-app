from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import pipeline
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(pipeline.router)

@app.get("/")
def health_check():
    return {"status": "OK"}