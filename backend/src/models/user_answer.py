from datetime import datetime
from uuid import UUID
from sqlalchemy import Text, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from core.database import Base

class UserAnswer(Base):
    __tablename__ = "user_answers"

    user_answer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(Integer, nullable=True)
    learner_key: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    user_answer: Mapped[str] = mapped_column(Text, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
