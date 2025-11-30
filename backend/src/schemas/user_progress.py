from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class UserProgressBase(BaseModel):
    learner_key: UUID4
    question_id: Optional[int] = None
    attempts_count: int = 0
    best_score: int = 0
    last_score: int = 0
    gap_to_mastery: int = 100
    status: str = 'new'
    last_answer_at: Optional[datetime] = None

class UserProgressCreate(UserProgressBase):
    pass

class UserProgressRead(UserProgressBase):
    user_progress_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
