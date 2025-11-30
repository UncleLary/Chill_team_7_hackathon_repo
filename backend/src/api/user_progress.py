from typing import List
from fastapi import APIRouter, Depends, status, FastAPI
from core.user_progress import UserProgressManager, get_user_progress_manager
from schemas.user_progress import UserProgressRead, UserProgressCreate

def get_user_progress_router() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/{user_progress_id}",
        response_model=UserProgressRead,
        name="user_progress:get_user_progress",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "User progress not found",
            },
        },
    )
    async def get_user_progress(
        user_progress_id: int,
        manager: UserProgressManager = Depends(get_user_progress_manager)
    ):
        return await manager.get_user_progress(user_progress_id)

    @router.get(
        "/",
        response_model=List[UserProgressRead],
        name="user_progress:list_user_progress",
    )
    async def list_user_progress(
        limit: int = 100,
        offset: int = 0,
        manager: UserProgressManager = Depends(get_user_progress_manager)
    ):
        return await manager.list_user_progress(limit, offset)

    @router.post(
        "/",
        response_model=UserProgressRead,
        status_code=status.HTTP_201_CREATED,
        name="user_progress:create_user_progress",
    )
    async def create_user_progress(
        user_progress_create: UserProgressCreate,
        manager: UserProgressManager = Depends(get_user_progress_manager)
    ):
        return await manager.create_user_progress(user_progress_create)

    @router.delete(
        "/{user_progress_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        name="user_progress:delete_user_progress",
        responses={
            status.HTTP_404_NOT_FOUND: {
                "description": "User progress not found",
            },
        },
    )
    async def delete_user_progress(
        user_progress_id: int,
        manager: UserProgressManager = Depends(get_user_progress_manager)
    ):
        await manager.delete_user_progress(user_progress_id)
        return None

    return router

def include_routers(app: FastAPI):
    app.include_router(get_user_progress_router(), prefix="/user_progress", tags=["user_progress"])
