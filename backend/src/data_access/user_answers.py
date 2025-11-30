from typing import List, Optional, Dict, Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.database import get_db
from models.user_answer import UserAnswer

class UserAnswerDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_answer_id: int) -> Optional[UserAnswer]:
        statement = select(UserAnswer).where(UserAnswer.user_answer_id == user_answer_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_answers(self, limit: int = 100, offset: int = 0) -> List[UserAnswer]:
        statement = select(UserAnswer).order_by(desc(UserAnswer.answered_at)).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, create_dict: Dict[str, Any]) -> UserAnswer:
        # Ensure ID and answered_at are not set manually if passed, relying on DB defaults
        create_dict.pop("user_answer_id", None)
        create_dict.pop("answered_at", None)
        
        user_answer = UserAnswer(**create_dict)
        self.session.add(user_answer)
        await self.session.flush()
        await self.session.refresh(user_answer)
        return user_answer

    async def delete(self, user_answer: UserAnswer) -> None:
        await self.session.delete(user_answer)
        await self.session.flush()

async def get_user_answer_db(session: AsyncSession = Depends(get_db)):
    yield UserAnswerDatabase(session)
