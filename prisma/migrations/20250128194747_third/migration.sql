/*
  Warnings:

  - Added the required column `author_id` to the `Article` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Article" ADD COLUMN     "author_id" INTEGER NOT NULL;

-- AddForeignKey
ALTER TABLE "Article" ADD CONSTRAINT "Article_author_id_fkey" FOREIGN KEY ("author_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
