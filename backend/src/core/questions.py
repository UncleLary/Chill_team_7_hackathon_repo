from typing import List
from fastapi import Depends, HTTPException, status
from data_access.questions import QuestionDatabase, get_question_db
from schemas.questions import QuestionRead, QuestionCreate
from models.question import Question

class QuestionManager:
    def __init__(self, question_db: QuestionDatabase):
        self.question_db = question_db

    async def get_question(self, question_id: int) -> Question:
        question = await self.question_db.get(question_id)
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        return question

    async def list_questions(self, limit: int = 100, offset: int = 0) -> List[QuestionRead]:
        questions = await self.question_db.list_questions(limit, offset)
        return [QuestionRead.model_validate(q) for q in questions]

    async def create_question(self, question_data: QuestionCreate) -> QuestionRead:
        create_dict = question_data.model_dump()
        question = await self.question_db.create(create_dict)
        return QuestionRead.model_validate(question)

    async def delete_question(self, question_id: int) -> None:
        question = await self.question_db.get(question_id)
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        await self.question_db.delete(question)

async def get_question_manager(question_db: QuestionDatabase = Depends(get_question_db)):
    yield QuestionManager(question_db)
