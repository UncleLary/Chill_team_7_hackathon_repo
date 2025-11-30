from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class QuestionCreate(BaseModel):
    question: str
    correct_answer: str
    context: str = ""
    document_id: int

class QuestionRead(BaseModel):
    question_id: int
    question: str
    correct_answer: str
    context: str
    created_at: datetime
    document_id: int

    class Config:
        from_attributes = True
