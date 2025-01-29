from fastapi import APIRouter, HTTPException
from prisma.partials import ForumPartial
from app.db import db 


router = APIRouter(
    prefix="/forums",
    tags=["forums"],
)


@router.get("/")
async def get_all_forum():
    forums = await db.forum.find_many()

    if forums is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return forums


@router.get("/{forum_id}")
async def get_forum(forum_id: int):
    forum = await db.forum.find_first(where= {"id": forum_id})

    if forum is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return forum


@router.post("/")
async def create_forum(forum: ForumPartial):
    result = await db.forum.create(
        data={
        "name" : forum.name,
    },
    )
    return result


@router.patch("/")
async def patch_forum(forum: ForumPartial, forum_id: int):
    result = await db.forum.upsert(
        where={
            "id": forum_id
        },
        data={
            "create": {
                "name": forum.name,
            },
            "update": {
                "name": forum.name,
            },
        },
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@router.delete("/{forum_id}")
async def delete_forum(forum_id: int):

    await db.thread.delete_many(where={"forum_id": forum_id})
    
    forum = await db.forum.delete(where={"id": forum_id})

    if forum is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"description": f"Successfully deleted item: {forum_id}"}