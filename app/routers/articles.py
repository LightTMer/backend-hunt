from fastapi import APIRouter, HTTPException
from prisma.models import Article
from prisma.partials import ThreadPartial
from app.db import db 


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)


# SAMPLE CRUD BEGIN
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
async def post_article(article: Article):
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

    return result


@router.patch("/")
async def patch_article(article: Article):
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

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@router.delete("/{article_id}")
async def delete_article(article_id: int):
    result = await db.article.delete(where={"id": article_id})

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"description": f"Successfully deleted item: {article_id}"}