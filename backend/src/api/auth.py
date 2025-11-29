import os

from fastapi import FastAPI, Body, Depends, APIRouter, status, Request
from fastapi_users.router.common import ErrorCode, ErrorModel
from fastapi_users import exceptions, schemas
from fastapi_users.openapi import OpenAPIResponseType

from core.auth import auth_backend, google_oauth_client, PASSWORD_AUTH_TOKEN_SECRET, fastapi_users, UserManager, get_user_manager
from schemas.user import UserCreate, UserCreateWithExtraArgs, UserRead, ForgotPasswordRequest

from util.exceptions import UserAlreadyExistsException, InvalidPasswordException
from util.exceptions import InvalidPasswordResetTokenException


def get_register_router() -> APIRouter:
    router = APIRouter()

    @router.post(
        "/register",
        response_model=UserRead,
        status_code=status.HTTP_201_CREATED,
        name="register:register",
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "model": ErrorModel,
                "content": {
                    "application/json": {
                        "examples": {
                            ErrorCode.REGISTER_USER_ALREADY_EXISTS: {
                                "summary": "A user with this email already exists.",
                                "value": {
                                    "detail": ErrorCode.REGISTER_USER_ALREADY_EXISTS
                                },
                            },
                            ErrorCode.REGISTER_INVALID_PASSWORD: {
                                "summary": "Password validation failed.",
                                "value": {
                                    "detail": {
                                        "code": ErrorCode.REGISTER_INVALID_PASSWORD,
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
    async def register(
        request: Request,
        payload : UserCreateWithExtraArgs,
        user_manager: UserManager = Depends(get_user_manager),
    ):
        # Note that this logic is here because we don't want to duplicate the UserManager from FastapiUsers.
        # We are stripping and handling extra fields from the payload which "stock" UserManager doesn't like.
        user_create_without_extra_args = UserCreate.model_validate(payload.model_dump())
        try:
            created_user = await user_manager.create(
                user_create_without_extra_args, safe=True, request=request
            )
                
        except exceptions.UserAlreadyExists:
            raise UserAlreadyExistsException("User with this email already exists")
        except exceptions.InvalidPasswordException as e:
            raise InvalidPasswordException("This password is not valid")

        return schemas.model_validate(UserRead, created_user)

    return router

RESET_PASSWORD_RESPONSES: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.RESET_PASSWORD_BAD_TOKEN: {
                        "summary": "Bad or expired token.",
                        "value": {"detail": ErrorCode.RESET_PASSWORD_BAD_TOKEN},
                    },
                    ErrorCode.RESET_PASSWORD_INVALID_PASSWORD: {
                        "summary": "Password validation failed.",
                        "value": {
                            "detail": {
                                "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                                "reason": "Password should be at least 3 characters",
                            }
                        },
                    },
                }
            }
        },
    },
}

def get_reset_password_router() -> APIRouter:
    router = APIRouter()

    @router.post(
        "/forgot-password",
        status_code=status.HTTP_202_ACCEPTED,
        name="reset:forgot_password",
    )
    async def forgot_password(
        request: Request,
        payload : ForgotPasswordRequest,
        user_manager: UserManager = Depends(get_user_manager),
    ):
        try:
            user = await user_manager.get_by_email(payload.email)
        except exceptions.UserNotExists:
            return None

        try:
            await user_manager.forgot_password(user, request)
        except exceptions.UserInactive:
            pass

        return None

    @router.post(
        "/reset-password",
        name="reset:reset_password",
        responses=RESET_PASSWORD_RESPONSES,
    )
    async def reset_password(
        request: Request,
        token: str = Body(...),
        password: str = Body(...),
        user_manager: UserManager = Depends(get_user_manager),
    ):
        try:
            await user_manager.reset_password(token, password, request)
        except (
            exceptions.InvalidResetPasswordToken,
            exceptions.UserNotExists,
            exceptions.UserInactive,
        ):
            raise InvalidPasswordResetTokenException("Invalid password reset token")
        except exceptions.InvalidPasswordException as e:
            raise InvalidPasswordException(f"Invalid password: {e.reason}")

    return router

def include_routers(app : FastAPI):
    app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"])
    app.include_router(get_register_router(), prefix="/auth", tags=["auth"])
    app.include_router(get_reset_password_router(), prefix="/auth", tags=["auth"])
    app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
    app.include_router(fastapi_users.get_oauth_router(google_oauth_client, auth_backend, PASSWORD_AUTH_TOKEN_SECRET, 
                                                      redirect_url=os.getenv("APP_BASE_URL", None)), 
                                                      prefix="/auth/google", tags=["auth"])
