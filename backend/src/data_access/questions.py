from typing import List, Optional, Dict, Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.database import get_db
from models.question import Question

class QuestionDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, question_id: int) -> Optional[Question]:
        statement = select(Question).where(Question.question_id == question_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_questions(self, limit: int = 100, offset: int = 0) -> List[Question]:
        statement = select(Question).order_by(desc(Question.created_at)).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, create_dict: Dict[str, Any]) -> Question:
        # Ensure created_at is not set manually if passed, relying on DB defaults
        create_dict.pop("created_at", None)
        create_dict.pop("question_id", None)
        
        question = Question(**create_dict)
        self.session.add(question)
        await self.session.flush()
        await self.session.refresh(question)
        return question

    async def delete(self, question: Question) -> None:
        await self.session.delete(question)
        await self.session.flush()

async def get_question_db(session: AsyncSession = Depends(get_db)):
    yield QuestionDatabase(session)
