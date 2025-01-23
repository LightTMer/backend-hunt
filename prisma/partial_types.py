from prisma.models import Thread, Forum

Thread.create_partial(
    "ThreadPartial",
    exclude={"posts","forum","id"}
)

Forum.create_partial(
    "ForumPartial",
    exclude={"threads","id"}
)