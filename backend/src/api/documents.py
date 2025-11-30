from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, FastAPI
from core.documents import DocumentManager, get_document_manager
from schemas.documents import DocumentRead, DocumentList
from fastapi.responses import Response

def get_documents_router() -> APIRouter:
    router = APIRouter()


    @router.get(
        "/{document_id}",
        response_model=DocumentRead,
        name="documents:get_document",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "Document not found",
            },
        },
    )
    async def get_document(
        document_id: int,
        manager: DocumentManager = Depends(get_document_manager)
    ):
        db_doc = await manager.get_document(document_id)
        return Response(content=db_doc.data, media_type=db_doc.content_type)

    @router.get(
        "/",
        response_model=List[DocumentList],
        name="documents:list_documents",
    )
    async def list_documents(
        limit: int = 100,
        offset: int = 0,
        manager: DocumentManager = Depends(get_document_manager)
    ):
        return await manager.list_documents(limit, offset)

    @router.post(
        "/",
        response_model=DocumentRead,
        status_code=status.HTTP_201_CREATED,
        name="documents:create_document",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "description": "Invalid file type",
            },
        },
    )
    async def create_document(
        description: str = Form(...),
        file: UploadFile = File(...),
        manager: DocumentManager = Depends(get_document_manager)
    ):
        return await manager.create_document(description, file)

    @router.delete(
        "/{document_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        name="documents:delete_document",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "Document not found",
            },
        },
    )
    async def delete_document(
        document_id: int,
        manager: DocumentManager = Depends(get_document_manager)
    ):
        await manager.delete_document(document_id)
        return None

    return router

def include_routers(app: FastAPI):
    app.include_router(get_documents_router(), prefix="/documents", tags=["documents"])
