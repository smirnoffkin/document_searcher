from elasticsearch import BadRequestError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.connection import get_db
from app.db.postgres.models import Post
from app.db.elasticsearch.connection import elastic
from app.db.elasticsearch.models import MAPPING_FOR_INDEX
from app.schemas.post import (
    InsertDocumentRequest,
    DocumentStatusResponse,
    ShowDocuments
)
from app.services.post import (
    create_document,
    delete_document,
    search_documents
)

router = APIRouter(tags=["Posts (Documents)"])


@router.post(
    "/create_document",
    description="Create post",
    response_model=DocumentStatusResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_post(
    body: InsertDocumentRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        document_id = await create_document(body, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="check timezone at created_date"
        )
    return {"success": True, "document_id": document_id}


@router.post(
    "/create_indexes",
    description="Create elasticsearch indexes",
    status_code=status.HTTP_201_CREATED
)
async def create_elasticsearch_indexes(index_name: str) -> dict:
    try:
        await elastic.indices.create(
            index=index_name,
            mappings=MAPPING_FOR_INDEX
        )
    except BadRequestError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This index already exists"
        )
    return {"success": True}


@router.get(
    "/search_documents/{search_query}",
    description="Get all posts",
    response_model=ShowDocuments,
    status_code=status.HTTP_200_OK
)
@cache(expire=10)
async def get_all_posts(
    search_query: str,
    db: AsyncSession = Depends(get_db)
):
    documents: list[Post] | None = await search_documents(search_query, db)
    if documents is None:
        return {"success": True, "documents": []}
    return {"success": True,
            "documents": [
            {
                "id": document.id,
                "rubrics": document.rubrics,
                "text": document.text,
                "created_date": document.created_date
            } for document in documents
        ]}


@router.delete(
    "/delete_document/{document_id}",
    description="Delete post",
    response_model=DocumentStatusResponse,
    status_code=status.HTTP_200_OK
)
async def delete_post(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted_document_id = await delete_document(document_id, db)
    if deleted_document_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {document_id} not found."
        )
    return {"success": True, "document_id": deleted_document_id}
