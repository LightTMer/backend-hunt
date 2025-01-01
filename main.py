from fastapi import FastAPI
from pydantic import BaseModel


class Article(BaseModel):
    id: int
    name: str
    tags: list[str]
    text: str | None = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, Client!"}


# SAMPLE CRUD BEGIN
@app.get("/articles/")
async def get_all_articles():
    return None


@app.get("/articles/{article_id}")
async def get_article(article_id: int):
    return {"article_id": article_id}


@app.post("/articles/")
async def post_article(article: Article):
    return article


@app.patch("/articles/")
async def patch_article(article: Article):
    return article


@app.delete("/articles/{article_id}")
async def delete_article(article_id: int):
    return {"article_id": article_id}
