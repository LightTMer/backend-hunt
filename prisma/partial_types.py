from prisma.models import Thread, Forum, Post

Thread.create_partial(
    "ThreadPartial",
    exclude={"posts","forum","id"}
)

Forum.create_partial(
    "ForumPartial",
    exclude={"threads","id"}
)

Post.create_partial(
    "PostPartial",
    exclude={"author","thread","article", "id"}
)