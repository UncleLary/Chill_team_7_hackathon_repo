from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy import Integer, String, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    user_progress_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    learner_key: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    question_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    attempts_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    best_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    gap_to_mastery: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    status: Mapped[str] = mapped_column(String, nullable=False, default='new')
    
    last_answer_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint('learner_key', 'question_id', name='user_progress_learner_key_question_id_key'),
    )
