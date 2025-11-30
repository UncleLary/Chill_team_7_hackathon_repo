from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class UserAnswerCreate(BaseModel):
    question_id: Optional[int] = None
    learner_key: UUID
    user_answer: str

class UserAnswerRead(BaseModel):
    user_answer_id: int
    question_id: Optional[int]
    learner_key: UUID
    user_answer: str
    answered_at: datetime

    class Config:
        from_attributes = True
