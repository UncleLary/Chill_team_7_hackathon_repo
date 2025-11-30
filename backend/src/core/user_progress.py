from typing import List
from fastapi import Depends, HTTPException, status
from data_access.user_progress import UserProgressDatabase, get_user_progress_db
from schemas.user_progress import UserProgressRead, UserProgressCreate
from models.user_progress import UserProgress

class UserProgressManager:
    def __init__(self, user_progress_db: UserProgressDatabase):
        self.user_progress_db = user_progress_db

    async def get_user_progress(self, user_progress_id: int) -> UserProgress:
        user_progress = await self.user_progress_db.get(user_progress_id)
        if not user_progress:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User progress not found")
        return user_progress

    async def list_user_progress(self, limit: int = 100, offset: int = 0) -> List[UserProgressRead]:
        user_progress_list = await self.user_progress_db.list_user_progress(limit, offset)
        return [UserProgressRead.model_validate(up) for up in user_progress_list]

    async def create_user_progress(self, user_progress_create: UserProgressCreate) -> UserProgressRead:
        create_dict = user_progress_create.model_dump()
        user_progress = await self.user_progress_db.create(create_dict)
        return UserProgressRead.model_validate(user_progress)

    async def delete_user_progress(self, user_progress_id: int) -> None:
        user_progress = await self.user_progress_db.get(user_progress_id)
        if not user_progress:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User progress not found")
        await self.user_progress_db.delete(user_progress)

async def get_user_progress_manager(user_progress_db: UserProgressDatabase = Depends(get_user_progress_db)):
    yield UserProgressManager(user_progress_db)
