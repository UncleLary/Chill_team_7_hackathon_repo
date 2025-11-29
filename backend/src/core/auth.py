import os
from typing_extensions import override
import uuid
from typing import Optional, Dict, Any, List

from httpx_oauth.clients.google import GoogleOAuth2

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.db import SQLAlchemyUserDatabase

from core.database import PAGE_SIZE, NON_PAGED_LIMIT
from data_access.users import get_auth_database_strategy, get_user_db
from models.user import User
from schemas.user import UserRead, UserListFilter, UserListPage
from util.user import user_to_user_read

PASSWORD_AUTH_TOKEN_SECRET = os.environ["PASSWORD_AUTH_TOKEN_SECRET"]

bearer_transport = BearerTransport(tokenUrl="auth/login")

auth_backend = AuthenticationBackend(
    name="dbtoken",
    transport=bearer_transport,
    get_strategy=get_auth_database_strategy,
)

google_oauth_client = GoogleOAuth2(
    os.getenv("GOOGLE_OAUTH_CLIENT_ID", ""),
    os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", ""),
)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = PASSWORD_AUTH_TOKEN_SECRET
    verification_token_secret = PASSWORD_AUTH_TOKEN_SECRET

    @override
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        await self.update_profile_complete(user)

    @override
    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgotten their password")
#        send_email_templated(user.email, 'forgot_password', data={"email":user.email,"name":user.full_name,"token":token})
        

    @override
    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}.")
#        send_email_templated(user.email, 'verify_email', data={"email":user.email,"name":user.full_name,"token":token})

    @override
    async def on_after_update(
        self, user: User, update_dict: Dict[str, Any], request: Optional[Request] = None):
        print(f"User {user.id} updated")
        await self.update_profile_complete(user)

    async def update_profile_complete(self, user: User):
        # By default, user needs full name and email to have complete profile.
        profile_complete = len(user.email)>0 and len(user.full_name)>0

        if profile_complete != user.is_profile_complete:
            print(f"Profile setting complete to {profile_complete}")
            return await self._update(user, {"is_profile_complete":profile_complete})
        return user
    
    async def list_users(self, filter : UserListFilter, page_no : int = None) -> List[UserRead] | UserListPage:
        offset = 0 if page_no is None else PAGE_SIZE * page_no
        # We use PAGE_SIZE + 1 here to detect if there is more data (we will return only PAGE_SIZE rows)
        limit = NON_PAGED_LIMIT if page_no is None else PAGE_SIZE+1
        results = await self.user_db.list_users(filter.is_active,
                                                filter.rec_date_start, filter.rec_date_end, 
                                                filter.text_filter, offset, limit)
        if page_no is None:
            return [user_to_user_read(result) for result in results]
        else:
            return UserListPage(content=[user_to_user_read(result) for result in results[:PAGE_SIZE]],
                                is_more_data_available=len(results)>PAGE_SIZE)



async def get_user_manager(user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])