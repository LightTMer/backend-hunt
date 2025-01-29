from fastapi import APIRouter, HTTPException
from prisma.partials import ThreadPartial
from app.db import db 


router = APIRouter(
    prefix="/threads",
    tags=["threads"],
)


@router.get("/")
async def get_all_threads():
    threads = await db.thread.find_many()

    if threads is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return threads


@router.get("/{thread_id}")
async def get_thread(thread_id: int):
    thread = await db.thread.find_first(where= {"id": thread_id})

    if thread is None: 
        raise HTTPException(status_code=404, detail="Item not found")
    return thread 


@router.delete("/{thread_id}")
async def delete_thread(thread_id: int):

    await db.post.delete_many(where={"thread_id": thread_id}) 

    thread = await db.thread.delete(where= {"id": thread_id})

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    return {"detail": f"Thread id: {thread_id} deleted"}


@router.post("/")
async def create_thread(thread: ThreadPartial):

    forum_exists = await db.forum.find_first(where={"id": thread.forum_id})
    if not forum_exists:
        raise HTTPException(status_code=404, detail="Forum not found")
    
    result = await db.thread.create(
        data={
            "name": thread.name,
            "description": thread.description,
            "total_upvotes": thread.total_upvotes,
            "total_downvotes": thread.total_downvotes,
            "rating": thread.rating,
            "forum_id": thread.forum_id,
        }
    )
    return result


@router.patch("/")
async def path_thread(thread: ThreadPartial, thread_id: int):

    forum_exists = await db.forum.find_first(where={"id": thread.forum_id})
    if not forum_exists:
        raise HTTPException(status_code=404, detail="Forum not found")
    
    result = await db.thread.upsert(
        where= {
            "id": thread_id
        },
        data={
            "create": {
            "name": thread.name,
            "description": thread.description,
            "total_upvotes": thread.total_upvotes,
            "total_downvotes": thread.total_downvotes,
            "rating": thread.rating,
            "forum_id": thread.forum_id,
        },
        "update" : {
            "name": thread.name,
            "description": thread.description,
            "total_upvotes": thread.total_upvotes,
            "total_downvotes": thread.total_downvotes,
            "rating": thread.rating,
            "forum_id": thread.forum_id,
        },
        },
    )
    
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result