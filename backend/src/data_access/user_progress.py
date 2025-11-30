from typing import List, Optional, Dict, Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.database import get_db
from models.user_progress import UserProgress

class UserProgressDatabase:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_progress_id: int) -> Optional[UserProgress]:
        statement = select(UserProgress).where(UserProgress.user_progress_id == user_progress_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_user_progress(self, limit: int = 100, offset: int = 0) -> List[UserProgress]:
        statement = select(UserProgress).order_by(desc(UserProgress.updated_at)).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, create_dict: Dict[str, Any]) -> UserProgress:
        # Ensure ID and timestamps are not set manually if passed, relying on DB defaults
        create_dict.pop("user_progress_id", None)
        create_dict.pop("created_at", None)
        create_dict.pop("updated_at", None)
        
        user_progress = UserProgress(**create_dict)
        self.session.add(user_progress)
        await self.session.flush()
        await self.session.refresh(user_progress)
        return user_progress

    async def update(self, user_progress: UserProgress, update_dict: Dict[str, Any]) -> UserProgress:
        for key, value in update_dict.items():
            setattr(user_progress, key, value)
        
        await self.session.flush()
        await self.session.refresh(user_progress)
        return user_progress

    async def delete(self, user_progress: UserProgress) -> None:
        await self.session.delete(user_progress)
        await self.session.flush()

async def get_user_progress_db(session: AsyncSession = Depends(get_db)):
    yield UserProgressDatabase(session)
