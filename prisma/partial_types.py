from prisma.models import Thread, Forum, Post, Article, Language, User

Article.create_partial(
    "ArticlePartial",
    exclude={"language", "post", "id"},
    optional={"views"},
)

Thread.create_partial(
    "ThreadPartial",
    exclude={"posts", "forum", "id"},
    optional={"description", "total_upvotes", "total_downvotes"},
)

Language.create_partial(
    "LanguagePartial",
    exclude={"id", "articles"},
)

User.create_partial(
    "UserPartial",
    exclude={"id", "salt", "posts"},
)

Forum.create_partial(
    "ForumPartial",
    exclude={"threads", "id"},
)

Post.create_partial(
    "PostPartial",
    exclude={"author", "thread", "article", "id"},
    optional={"body", "upvotes", "downvotes", "rating"},
)
