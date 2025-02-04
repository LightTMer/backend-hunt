from fastapi import APIRouter, HTTPException

from prisma.partials import ArticlePartial
from app.db import db


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_all_articles():
    articles = await db.article.find_many()

    if articles is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return articles


@router.get("/{article_id}")
async def get_article(article_id: int):
    article = await db.article.find_first(where={"id": article_id})

    if article is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return article


@router.post("/")
async def post_article(article: ArticlePartial):
    thread_create = await db.thread.create(
        data={
            "name": article.title,
            "forum_id": 1,
        },
    )
    post_create = await db.post.create(
        data={
            "title": article.title,
            "author_id": article.author_id,
            "thread_id": thread_create.id,
        },
    )
    result = await db.article.create(
        data={
            "title": article.title,
            "body": article.body,
            "published": article.published,
            "author_id": article.author_id,
            "language_id": article.language_id,
            "post_id": post_create.id,
            "views": article.views,
        },
    )

    return result


@router.patch("/")
async def patch_article(article: ArticlePartial, article_id: int):
    # uses UPSERT for creating the record in case one does not exist
    result = await db.article.upsert(
        where={
            "id": article_id,
        },
        data={
            "create": {
                "title": article.title,
                "body": article.body,
                "published": article.published,
                "author_id": article.author_id,
                "language_id": article.language_id,
                "post_id": article.post_id,
                "views": article.views,
            },
            "update": {
                "title": article.title,
                "body": article.body,
                "published": article.published,
                "author_id": article.author_id,
                "language_id": article.language_id,
                "post_id": article.post_id,
                "views": article.views,
            },
        },
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@router.delete("/{article_id}")
async def delete_article(article_id: int):
    article = await db.article.find_first(where={"id": article_id})
    article_post = await db.post.find_first(where={"id": article.post_id})
    await db.post.delete_many(where={"thread_id": article_post.thread_id})
    await db.post.delete(where={"id": article_post.thread_id})
    result = await db.article.delete(where={"id": article_id})

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": f"Article id: {article_id} deleted"}
