from typing import List

from fastapi import FastAPI, Depends, APIRouter, status, Request, Response
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users import exceptions, schemas

from core.auth import fastapi_users, UserManager, get_user_manager
from schemas.user import UserRead, UserUpdate, UserListFilter, UserListPage
from models.user import User

from util.exceptions import UserDoesntExistsException, InvalidPasswordException, EmailAlreadyExistsException


def get_users_router(
    requires_verification: bool = False,
) -> APIRouter:
    """Generate a router with the authentication routes."""
    router = APIRouter()

    get_current_active_user = fastapi_users.authenticator.current_user(
        active=True, verified=requires_verification
    )
    get_current_superuser = fastapi_users.authenticator.current_user(
        active=True, verified=requires_verification, superuser=True
    )

    async def get_user_or_404(
        id: str,
        user_manager: UserManager = Depends(get_user_manager),
    ) -> User:
        try:
            parsed_id = user_manager.parse_id(id)
            return await user_manager.get(parsed_id)
        except (exceptions.UserNotExists, exceptions.InvalidID):
            raise UserDoesntExistsException(f"User with ID={id} was not found!")

    @router.get(
        "/me",
        response_model=UserRead,
        name="users:current_user",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
        },
    )
    async def me(
        user: User = Depends(get_current_active_user),
    ):
        return schemas.model_validate(UserRead, user)

    @router.patch(
        "/me",
        response_model=UserRead,
        dependencies=[Depends(get_current_active_user)],
        name="users:patch_current_user",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": {
                                        "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                        "reason": "Password should be"
                                        "at least 3 characters",
                                    }
                                },
                            },
                        }
                    }
                },
            },
        },
    )
    async def update_me(
        request: Request,
        user_update: UserUpdate,  # type: ignore
        user: User = Depends(get_current_active_user),
        user_manager: UserManager = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.update(
                user_update, user, safe=True, request=request
            )
            return schemas.model_validate(UserRead, user)
        except exceptions.InvalidPasswordException:
            raise InvalidPasswordException("Invalid password during user update")
        except exceptions.UserAlreadyExists:
            raise EmailAlreadyExistsException(f"Email {user_update.email} is already used by a different account.")

    @router.get(
        "/",
        response_model=List[UserRead],
        name="users:list",
        dependencies=[Depends(get_current_superuser)],
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
        },
    )
    async def list_users(
        payload : UserListFilter = Depends(UserListFilter),        
        user_manager: UserManager = Depends(get_user_manager),
    ) -> List[UserRead]:
        return await user_manager.list_users(payload)

    @router.get(
        "/page/{page_no}",
        response_model=UserListPage,
        name="users:list_paged",
        dependencies=[Depends(get_current_superuser)],
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
        },
    )
    async def list_users_paged(
        page_no : int,
        payload : UserListFilter = Depends(UserListFilter),        
        user_manager: UserManager = Depends(get_user_manager),
    ) -> UserListPage:
        return await user_manager.list_users(payload, page_no)

    @router.get(
        "/{id}",
        response_model=UserRead,
        dependencies=[Depends(get_current_superuser)],
        name="users:user",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
            status.HTTP_403_FORBIDDEN: {
                "description": "Not a superuser.",
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "The user does not exist.",
            },
        },
    )
    async def get_user(user=Depends(get_user_or_404)):
        return schemas.model_validate(UserRead, user)

    @router.patch(
        "/{id}",
        response_model=UserRead,
        dependencies=[Depends(get_current_superuser)],
        name="users:patch_user",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
            status.HTTP_403_FORBIDDEN: {
                "description": "Not a superuser.",
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "The user does not exist.",
            },
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": {
                                        "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                        "reason": "Password should be"
                                        "at least 3 characters",
                                    }
                                },
                            },
                        }
                    }
                },
            },
        },
    )
    async def update_user(
        user_update: UserUpdate,  # type: ignore
        request: Request,
        user=Depends(get_user_or_404),
        user_manager: UserManager = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.update(
                user_update, user, safe=False, request=request
            )
            return schemas.model_validate(UserRead, user)
        except exceptions.InvalidPasswordException:
            raise InvalidPasswordException("Password invalid during update")
        except exceptions.UserAlreadyExists:
            raise EmailAlreadyExistsException(f"Email {user_update.email} is already used by a different account.")

    @router.delete(
        "/{id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        dependencies=[Depends(get_current_superuser)],
        name="users:delete_user",
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
            status.HTTP_403_FORBIDDEN: {
                "description": "Not a superuser.",
            },
            status.HTTP_404_NOT_FOUND: {
                "description": "The user does not exist.",
            },
        },
    )
    async def delete_user(
        request: Request,
        user=Depends(get_user_or_404),
        user_manager: UserManager = Depends(get_user_manager),
    ):
        await user_manager.delete(user, request=request)
        return None

    return router


def include_routers(app : FastAPI):
    app.include_router(get_users_router(), prefix="/users", tags=["users"])
