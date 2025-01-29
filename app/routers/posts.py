from fastapi import APIRouter, HTTPException
from prisma.partials import PostPartial
from app.db import db 


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)



@router.get("/")
async def get_posts():
    posts = await db.post.find_many()

    if posts is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return posts


@router.get("/{post_id}")
async def get_post(post_id: int):
    post = await db.post.find_first(where= {"id": post_id})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/")
async def create_post(post: PostPartial):
    result = await db.post.create(
        data={
            "title": post.title,
            "body": post.body,
            "upvotes": post.upvotes,
            "downvotes": post.downvotes,
            "rating": post.rating,
            "author_id": post.author_id,
            "thread_id": post.thread_id,
        }
    )
    return result


@router.patch("/")
async def patch_post(post: PostPartial, post_id: int):

    user_exists = await db.user.find_first(where={"id": post.author_id})
    thread_exists = await db.thread.find_first(where={"id": post.thread_id})

    if not (user_exists):
        raise HTTPException(status_code=404, detail="User not found")
    
    if not (thread_exists):
        raise HTTPException(status_code=404, detail="Thread not found")
        
    result = await db.post.upsert(
        where= {
            "id": post_id
        },
        data={
            "create": {
                "title": post.title,
                "body": post.body,
                "upvotes": post.upvotes,
                "downvotes": post.downvotes,
                "rating": post.rating,
                "author_id": post.author_id,
                "thread_id": post.thread_id,
            },
            "update": {
                "title": post.title,
                "body": post.body,
                "upvotes": post.upvotes,
                "downvotes": post.downvotes,
                "rating": post.rating,
                "author_id": post.author_id,
                "thread_id": post.thread_id,
            },
        },
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
    

@router.delete("/{post_id}")
async def delete_post(post_id: int):
    await db.article.delete_many(where={"post_id": post_id})
    posts = await db.post.delete(where={"id": post_id})

    if not posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": f"Post id: {post_id} deleted"}