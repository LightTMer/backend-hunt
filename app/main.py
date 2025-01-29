from prisma import Prisma
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import articles,forums,posts,threads
from app.db import connect_db, disconnect_db


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield  
    await disconnect_db()

app = FastAPI(lifespan=lifespan)

app.include_router(articles.router)
app.include_router(forums.router)
app.include_router(threads.router)
app.include_router(posts.router)


@app.get("/")
async def root():
    return {"message": "Hello, Client!"}