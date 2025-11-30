from typing import List, Optional, Dict, Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.database import get_db
from models.document import Document

class DocumentDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, document_id: int) -> Optional[Document]:
        statement = select(Document).where(Document.document_id == document_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_documents(self, limit: int = 100, offset: int = 0) -> List[Document]:
        statement = select(Document).order_by(desc(Document.rec_date)).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, create_dict: Dict[str, Any]) -> Document:
        # Ensure ID and rec_date are not set manually if passed, relying on DB defaults
        create_dict.pop("document_id", None)
        create_dict.pop("rec_date", None)
        
        document = Document(**create_dict)
        self.session.add(document)
        await self.session.flush()
        await self.session.refresh(document)
        return document

    async def delete(self, document: Document) -> None:
        await self.session.delete(document)
        await self.session.flush()

async def get_document_db(session: AsyncSession = Depends(get_db)):
    yield DocumentDatabase(session)
