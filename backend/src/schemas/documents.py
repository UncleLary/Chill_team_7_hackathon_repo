from pydantic import BaseModel, Field
from datetime import datetime

class DocumentList(BaseModel):
    document_id: int
    name: str
    description: str
    content_type: str
    rec_date: datetime

class DocumentRead(BaseModel):
    document_id: int
    name: str
    description: str
    content_type: str
    text_data: str
    rec_date: datetime

    class Config:
        from_attributes = True
