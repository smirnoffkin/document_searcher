from datetime import datetime

from pydantic import BaseModel


class InsertDocumentRequest(BaseModel):
    text: str
    created_date: datetime
    rubrics: list[str]


class DeleteDocumentRequest(BaseModel):
    document_id: int


class SearchDocumentsRequest(BaseModel):
    search_query: str


class DocumentStatusResponse(BaseModel):
    success: bool
    document_id: int

    class Config:
        orm_mode = True


class ShowDocuments(BaseModel):
    success: bool
    documents: list

    class Config:
        orm_mode = True
