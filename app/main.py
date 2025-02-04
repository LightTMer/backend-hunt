from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db import connect_db, disconnect_db
from app.routers import articles


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()


app = FastAPI(lifespan=lifespan)

app.include_router(articles.router)


@app.get("/")
async def root():
    return {"message": "Hello, Client!"}
