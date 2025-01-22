from prisma import Prisma
from prisma.models import Article, Post
from fastapi import FastAPI, HTTPException


app = FastAPI()
db = Prisma(auto_register=True)


@app.get("/")
async def root():
    return {"message": "Hello, Client!"}


# SAMPLE CRUD BEGIN
@app.get("/articles/")
async def get_all_articles():
    await db.connect()
    articles = await db.article.find_many()
    await db.disconnect()

    if articles is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return articles


@app.get("/articles/{article_id}")
async def get_article(article_id: int):
    await db.connect()
    article = await db.article.find_first(where={"id": article_id})
    await db.disconnect()

    if article is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return article


@app.post("/articles/")
async def post_article(article: Article):
    await db.connect()
    result = await db.article.create(
        data={
            "id": article.id,
            "title": article.title,
            "body": article.body,
            # "post": {
            #     'connect': {
            #         'id': post.id
            #     }
            # },
            "published": article.published,
            "language_id": article.language_id,
            "views": article.views,
        },
    )
    await db.disconnect()

    return result


@app.patch("/articles/")
async def patch_article(article: Article):
    await db.connect()
    # uses UPSERT for creating the record in case one does not exist
    result = await db.article.upsert(
        where={
            "id": article.id,
        },
        data={
            "create": {
                "id": article.id,
                "title": article.title,
                "body": article.body,
                # "post": {
                #     'connect': {
                #         'id': post.id
                #     }
                # },
                "published": article.published,
                "language_id": article.language_id,
                "views": article.views,
            },
            "update": {
                "id": article.id,
                "title": article.title,
                "body": article.body,
                # "post": {
                #     'connect': {
                #         'id': post.id
                #     }
                # },
                "published": article.published,
                "language_id": article.language_id,
                "views": article.views,
            },
        },
    )
    await db.disconnect()

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@app.delete("/articles/{article_id}")
async def delete_article(article_id: int):
    await db.connect()
    result = await db.article.delete(where={"id": article_id})
    await db.disconnect()

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"description": f"Successfully deleted item: {article_id}"}
