from prisma import Prisma
from prisma.models import Article, Post, Forum, Thread, Post
from fastapi import FastAPI, HTTPException

from prisma.partials import ThreadPartial, ForumPartial, PostPartial
from contextlib import asynccontextmanager


app = FastAPI()
db = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield  
    await db.disconnect()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, Client!"}


# SAMPLE CRUD BEGIN
@app.get("/articles/")
async def get_all_articles():
    articles = await db.article.find_many()

    if articles is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return articles


@app.get("/articles/{article_id}")
async def get_article(article_id: int):
    article = await db.article.find_first(where={"id": article_id})

    if article is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return article


@app.post("/articles/")
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


@app.patch("/articles/")
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


@app.delete("/articles/{article_id}")
async def delete_article(article_id: int):
    result = await db.article.delete(where={"id": article_id})

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"description": f"Successfully deleted item: {article_id}"}


@app.get("/forums/")
async def get_all_forum():
    forums = await db.forum.find_many()

    if forums is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return forums


@app.get("/forums/{forum_id}")
async def get_forum(forum_id: int):
    forum = await db.forum.find_first(where= {"id": forum_id})

    if forum is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return forum


@app.post("/forums/")
async def create_forum(forum: ForumPartial):
    result = await db.forum.create(
        data={
        "name" : forum.name,
    },
    )
    return result


@app.patch("/forums/")
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


@app.delete("/forums/{forum_id}")
async def delete_forum(forum_id: int):

    await db.thread.delete_many(where={"forum_id": forum_id})
    
    forum = await db.forum.delete(where={"id": forum_id})

    if forum is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"description": f"Successfully deleted item: {forum_id}"}


@app.get("/threads/")
async def get_all_threads():
    threads = await db.thread.find_many()

    if threads is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return threads


@app.get("/threads/{thread_id}")
async def get_thread(thread_id: int):
    thread = await db.thread.find_first(where= {"id": thread_id})

    if thread is None: 
        raise HTTPException(status_code=404, detail="Item not found")
    return thread 


@app.delete("/threads/{thread_id}")
async def delete_thread(thread_id: int):

    await db.post.delete_many(where={"thread_id": thread_id}) 

    thread = await db.thread.delete(where= {"id": thread_id})

    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    return {"detail": f"Thread id: {thread_id} deleted"}


@app.post("/threads/")
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


@app.patch("/threads/")
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


@app.get("/posts/")
async def get_posts():
    posts = await db.post.find_many()

    if posts is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return posts


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    post = await db.post.find_first(where= {"id": post_id})

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts/")
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


@app.patch("/posts/")
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
    

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    await db.article.delete_many(where={"post_id": post_id})
    posts = await db.post.delete(where={"id": post_id})

    if not posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": f"Post id: {post_id} deleted"}