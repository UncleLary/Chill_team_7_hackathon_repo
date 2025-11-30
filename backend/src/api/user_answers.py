from typing import List
from fastapi import APIRouter, Depends, status, FastAPI
from core.user_answers import UserAnswerManager, get_user_answer_manager
from schemas.user_answers import UserAnswerRead, UserAnswerCreate

def get_user_answers_router() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/{user_answer_id}",
        response_model=UserAnswerRead,
        name="user_answers:get_user_answer",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "User answer not found",
            },
        },
    )
    async def get_user_answer(
        user_answer_id: int,
        manager: UserAnswerManager = Depends(get_user_answer_manager)
    ):
        return await manager.get_user_answer(user_answer_id)

    @router.get(
        "/",
        response_model=List[UserAnswerRead],
        name="user_answers:list_user_answers",
    )
    async def list_user_answers(
        limit: int = 100,
        offset: int = 0,
        manager: UserAnswerManager = Depends(get_user_answer_manager)
    ):
        return await manager.list_user_answers(limit, offset)

    @router.post(
        "/",
        response_model=UserAnswerRead,
        status_code=status.HTTP_201_CREATED,
        name="user_answers:create_user_answer",
    )
    async def create_user_answer(
        user_answer_create: UserAnswerCreate,
        manager: UserAnswerManager = Depends(get_user_answer_manager)
    ):
        return await manager.create_user_answer(user_answer_create)

    @router.delete(
        "/{user_answer_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        name="user_answers:delete_user_answer",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "User answer not found",
            },
        },
    )
    async def delete_user_answer(
        user_answer_id: int,
        manager: UserAnswerManager = Depends(get_user_answer_manager)
    ):
        await manager.delete_user_answer(user_answer_id)
        return None

    return router

def include_routers(app: FastAPI):
    app.include_router(get_user_answers_router(), prefix="/user_answers", tags=["user_answers"])
