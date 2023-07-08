from sqlalchemy.ext.asyncio import AsyncSession

from app.db.elasticsearch.connection import elastic
from app.schemas.post import InsertDocumentRequest
from app.services.crud import PostCRUD


async def create_document(
    body: InsertDocumentRequest,
    db: AsyncSession
) -> int:
    async with db.begin():
        post_crud = PostCRUD(db)
        new_post = await post_crud.create_post(
            text=body.text,
            created_date=body.created_date,
            rubrics=body.rubrics
        )
        document_id = new_post.id
        document = {"iD": document_id, "text": body.text}
        await elastic.index(
            index="documents",
            document=document,
            refresh="wait_for"
        )

    return document_id


async def delete_document(
    document_id: int,
    db: AsyncSession,
) -> int | None:
    async with db.begin():
        post_crud = PostCRUD(db)
        deleted_document_id = await post_crud.delete_post(document_id)
        if deleted_document_id is None:
            return

        await elastic.delete_by_query(
            index="documents",
            query={"match": {"iD": deleted_document_id}}
        )
        await elastic.indices.refresh(index="documents")

        return deleted_document_id


async def search_documents(
    search_query: str,
    db: AsyncSession
) -> list | None:
    async with db.begin():
        post_crud = PostCRUD(db)
        docs_raw = await elastic.search(
            index="documents",
            source={"includes": ["iD"]},
            query={"match": {"text": search_query}},
            size=20
        )
        document_ids = [
            doc["_source"]["iD"] for doc in docs_raw.body["hits"]["hits"]
        ]
        if len(document_ids) == 0:
            return
        documents = await post_crud.get_posts_by_ids(document_ids)

        return list(documents)
