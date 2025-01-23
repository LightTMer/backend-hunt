/*
  Warnings:

  - You are about to drop the column `author_id` on the `Article` table. All the data in the column will be lost.
  - You are about to drop the column `threads` on the `Forum` table. All the data in the column will be lost.
  - You are about to drop the column `posts` on the `Thread` table. All the data in the column will be lost.
  - You are about to drop the column `posts` on the `User` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[post_id]` on the table `Article` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `post_id` to the `Article` table without a default value. This is not possible if the table is not empty.
  - Added the required column `author_id` to the `Post` table without a default value. This is not possible if the table is not empty.
  - Added the required column `thread_id` to the `Post` table without a default value. This is not possible if the table is not empty.
  - Added the required column `forum_id` to the `Thread` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Article" DROP COLUMN "author_id",
ADD COLUMN     "post_id" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "Forum" DROP COLUMN "threads";

-- AlterTable
ALTER TABLE "Post" ADD COLUMN     "author_id" INTEGER NOT NULL,
ADD COLUMN     "thread_id" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "Thread" DROP COLUMN "posts",
ADD COLUMN     "forum_id" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "User" DROP COLUMN "posts";

-- CreateIndex
CREATE UNIQUE INDEX "Article_post_id_key" ON "Article"("post_id");

-- AddForeignKey
ALTER TABLE "Article" ADD CONSTRAINT "Article_post_id_fkey" FOREIGN KEY ("post_id") REFERENCES "Post"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Article" ADD CONSTRAINT "Article_language_id_fkey" FOREIGN KEY ("language_id") REFERENCES "Language"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Thread" ADD CONSTRAINT "Thread_forum_id_fkey" FOREIGN KEY ("forum_id") REFERENCES "Forum"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Post" ADD CONSTRAINT "Post_author_id_fkey" FOREIGN KEY ("author_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Post" ADD CONSTRAINT "Post_thread_id_fkey" FOREIGN KEY ("thread_id") REFERENCES "Thread"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
