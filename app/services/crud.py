from datetime import datetime

from sqlalchemy import any_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.models import Post


class PostCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_post(
        self,
        text: str,
        created_date: datetime,
        rubrics: list[str]
    ) -> Post:
        new_post = Post(
            text=text,
            created_date=created_date,
            rubrics=rubrics
        )
        self.db_session.add(new_post)
        await self.db_session.commit()
        return new_post

    async def get_posts_by_ids(self, document_ids: list) -> Post | None:
        query = select(Post).where(Post.id == any_(document_ids))
        res = await self.db_session.execute(query)
        post_row = res.fetchall()
        if post_row is not None:
            return post_row[0]

    async def delete_post(self, post_id: int) -> int | None:
        query = delete(Post).where(Post.id == post_id).returning(Post.id)
        res = await self.db_session.execute(query)
        deleted_post_row = res.fetchone()
        if deleted_post_row is not None:
            return deleted_post_row[0]
