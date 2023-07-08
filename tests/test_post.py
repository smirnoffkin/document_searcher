import pytest
from elasticsearch import AsyncElasticsearch
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres.models import Post


@pytest.mark.parametrize("document_data, index_name", [
    ({
        "text": "some valid text for searching",
        "rubrics": ["python", "programming", "backend"],
        "created_date": "2032-11-23T10:20:30"
    }, "documents")
])
async def test_create_document(
    client: AsyncClient,
    session: AsyncSession,
    elastic: AsyncElasticsearch,
    document_data: dict,
    index_name: str
):
    await client.post("/create_indexes", json=index_name)
    res = await client.post("/create_document", json=document_data)
    data = res.json()
    assert res.status_code == status.HTTP_201_CREATED
    assert data["success"]
    document_id = data["document_id"]

    documents_from_elastic = await elastic.search(index="documents", query={"match": {"iD": document_id}})
    assert len(documents_from_elastic.body["hits"]["hits"]) == 1
    document_from_elastic = documents_from_elastic["hits"]["hits"][0]["_source"]
    assert document_from_elastic["text"] == document_data["text"]
    assert document_from_elastic["iD"] == document_id


@pytest.mark.parametrize("search_query, documents", [
    ("some valid searching", [{
        "id": 1,
        "text": "some valid text for searching",
        "rubrics": ["python", "programming", "backend"],
        "created_date": "2032-11-23T10:20:30"
    }])
])
async def test_search_text_in_documents(
    client: AsyncClient,
    search_query: str,
    documents: list[dict]
):
    res = await client.get(f"/search_documents/{search_query}")
    data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert data["success"]
    assert data["documents"] == documents


@pytest.mark.parametrize("document_id", [
    (1)
])
async def test_delete_document(
    client: AsyncClient,
    session: AsyncSession,
    elastic: AsyncElasticsearch,
    document_id: int
):
    res = await client.delete(f"/delete_document/{document_id}")
    data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert data["success"]

    async with session.begin():
        query = select(Post).where(Post.id == data["document_id"])
        res = await session.execute(query)
        document_returned_data = list(res.scalars().all())
        assert len(document_returned_data) == 0

    documents_from_elastic = await elastic.search(index="documents", query={"match": {"iD": data["document_id"]}})
    assert len(documents_from_elastic.body["hits"]["hits"]) == 0


@pytest.mark.parametrize("document_id", [
    (15),
    (777),
    (999999)
])
async def test_delete_document_not_exists(client: AsyncClient, document_id: int):
    res = await client.delete(f"/delete_document/{document_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": f"Document with id {document_id} not found."}
