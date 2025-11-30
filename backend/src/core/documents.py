from typing import List
from fastapi import Depends, HTTPException, status
from data_access.documents import DocumentDatabase, get_document_db
from schemas.documents import DocumentRead, DocumentList
from fastapi import UploadFile
from models.document import Document
from core.pdf import PDFProcessor, get_pdf_processor

class DocumentManager:
    def __init__(self, document_db: DocumentDatabase, pdf_processor: PDFProcessor):
        self.document_db = document_db
        self.pdf_processor = pdf_processor

    async def get_document(self, document_id: int) -> Document:
        document = await self.document_db.get(document_id)
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        return document

    async def list_documents(self, limit: int = 100, offset: int = 0) -> List[DocumentList]:
        documents = await self.document_db.list_documents(limit, offset)
        return [DocumentRead.model_validate(doc, strict=False) for doc in documents]

    async def create_document(self, description : str, file_data : UploadFile) -> DocumentRead:
        create_dict = {
            "name": file_data.filename,
            "description": description,
            "content_type": file_data.content_type,
            "data": await file_data.read(),
        }
        if create_dict["content_type"] == "application/pdf":
            text_data = await self.pdf_processor.extract_text_with_markers(create_dict["data"])
            create_dict["text_data"] = text_data
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type. Only PDF files are supported."
            )
        document = await self.document_db.create(create_dict)
        return DocumentRead.model_validate(document)

    async def delete_document(self, document_id: int) -> None:
        document = await self.document_db.get(document_id)
        if not document:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        await self.document_db.delete(document)

async def get_document_manager(document_db: DocumentDatabase = Depends(get_document_db), pdf_processor: PDFProcessor = Depends(get_pdf_processor)):
    yield DocumentManager(document_db, pdf_processor)
