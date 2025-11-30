from typing import List
from fastapi import Depends, HTTPException, status
from data_access.user_answers import UserAnswerDatabase, get_user_answer_db
from schemas.user_answers import UserAnswerRead, UserAnswerCreate
from models.user_answer import UserAnswer

class UserAnswerManager:
    def __init__(self, user_answer_db: UserAnswerDatabase):
        self.user_answer_db = user_answer_db

    async def get_user_answer(self, user_answer_id: int) -> UserAnswer:
        user_answer = await self.user_answer_db.get(user_answer_id)
        if not user_answer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User answer not found")
        return user_answer

    async def list_user_answers(self, limit: int = 100, offset: int = 0) -> List[UserAnswerRead]:
        user_answers = await self.user_answer_db.list_answers(limit, offset)
        return [UserAnswerRead.model_validate(ans) for ans in user_answers]

    async def create_user_answer(self, user_answer_create: UserAnswerCreate) -> UserAnswerRead:
        create_dict = user_answer_create.model_dump()
        user_answer = await self.user_answer_db.create(create_dict)
        return UserAnswerRead.model_validate(user_answer)

    async def delete_user_answer(self, user_answer_id: int) -> None:
        user_answer = await self.user_answer_db.get(user_answer_id)
        if not user_answer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User answer not found")
        await self.user_answer_db.delete(user_answer)

async def get_user_answer_manager(user_answer_db: UserAnswerDatabase = Depends(get_user_answer_db)):
    yield UserAnswerManager(user_answer_db)
