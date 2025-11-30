from typing import List
from fastapi import APIRouter, Depends, status, FastAPI
from core.questions import QuestionManager, get_question_manager
from schemas.questions import QuestionRead, QuestionCreate

def get_questions_router() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/{question_id}",
        response_model=QuestionRead,
        name="questions:get_question",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "Question not found",
            },
        },
    )
    async def get_question(
        question_id: int,
        manager: QuestionManager = Depends(get_question_manager)
    ):
        return await manager.get_question(question_id)

    @router.get(
        "/",
        response_model=List[QuestionRead],
        name="questions:list_questions",
    )
    async def list_questions(
        limit: int = 100,
        offset: int = 0,
        manager: QuestionManager = Depends(get_question_manager)
    ):
        return await manager.list_questions(limit, offset)

    @router.post(
        "/",
        response_model=QuestionRead,
        status_code=status.HTTP_201_CREATED,
        name="questions:create_question",
    )
    async def create_question(
        question: QuestionCreate,
        manager: QuestionManager = Depends(get_question_manager)
    ):
        return await manager.create_question(question)

    @router.delete(
        "/{question_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        name="questions:delete_question",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "Question not found",
            },
        },
    )
    async def delete_question(
        question_id: int,
        manager: QuestionManager = Depends(get_question_manager)
    ):
        await manager.delete_question(question_id)
        return None

    return router

def include_routers(app: FastAPI):
    app.include_router(get_questions_router(), prefix="/questions", tags=["questions"])
