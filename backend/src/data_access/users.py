import os
from typing import Any, Dict, Generic, Optional, Type, List
from datetime import datetime

from fastapi import Depends
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from fastapi_users.db.base import BaseUserDatabase
from fastapi_users.models import ID, OAP, UP
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase, 
    DatabaseStrategy,
    AP
)
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTable

from core.database import get_db
from models.user import AccessToken, OAuthAccount, User

class TokenDatabase(Generic[AP], AccessTokenDatabase[AP]):

    def __init__(
        self,
        session: AsyncSession,
        access_token_table: Type[AP],
    ):
        self.session = session
        self.access_token_table = access_token_table

    async def get_by_token(
        self, token: str, max_age: Optional[datetime] = None
    ) -> Optional[AP]:
        statement = select(self.access_token_table).where(
            self.access_token_table.token == token  # type: ignore
        )
        if max_age is not None:
            statement = statement.where(
                self.access_token_table.created_at >= max_age  # type: ignore
            )

        results = await self.session.execute(statement)
        return results.scalar_one_or_none()

    async def create(self, create_dict: Dict[str, Any]) -> AP:
        access_token = self.access_token_table(**create_dict)
        self.session.add(access_token)
        await self.session.flush()
        await self.session.refresh(access_token)
        return access_token

    async def update(self, access_token: AP, update_dict: Dict[str, Any]) -> AP:
        for key, value in update_dict.items():
            setattr(access_token, key, value)
        self.session.add(access_token)
        await self.session.flush()
        await self.session.refresh(access_token)
        return access_token

    async def delete(self, access_token: AP) -> None:
        await self.session.delete(access_token)
        await self.session.flush()


class UserDatabase(Generic[UP, ID], BaseUserDatabase[UP, ID]):
    user_table: Type[UP]
    oauth_account_table: Optional[Type[SQLAlchemyBaseOAuthAccountTable]]

    def __init__(
        self,
        session: AsyncSession,
        user_table: Type[UP],
        oauth_account_table: Optional[Type[SQLAlchemyBaseOAuthAccountTable]] = None,
    ):
        self.user_table = user_table
        self.oauth_account_table = oauth_account_table

    async def get(self, id: ID) -> Optional[UP]:
        statement = select(self.user_table).where(self.user_table.id == id)
        return await self._get_user(statement)

    async def get_by_email(self, email: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.email) == func.lower(email)
        )
        return await self._get_user(statement)

    async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional[UP]:
        if self.oauth_account_table is None:
            raise NotImplementedError()

        statement = (
            select(self.user_table)
            .join(self.oauth_account_table)
            .where(self.oauth_account_table.oauth_name == oauth)  # type: ignore
            .where(self.oauth_account_table.account_id == account_id)  # type: ignore
        )
        return await self._get_user(statement)

    async def create(self, create_dict: Dict[str, Any]) -> UP:
        user = self.user_table(**create_dict)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update(self, user: UP, update_dict: Dict[str, Any]) -> UP:
        for key, value in update_dict.items():
            setattr(user, key, value)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def delete(self, user: UP) -> None:
        await self.session.delete(user)
        await self.session.flush()

    async def list_users(self, is_active : bool | None = True, 
                         rec_date_start : datetime | None = None, rec_date_end : datetime | None = None, 
                         text_filter : str = "", offset : int = 0, limit : int = 30) -> List[User]:
        statement = select(self.user_table).order_by(self.user_table.id).limit(limit)
        if is_active is not None:
            statement = statement.where(self.user_table.is_active == is_active)
        if rec_date_start is not None:
            statement = statement.where(self.user_table.rec_date > rec_date_start)
        if rec_date_end is not None:
            statement = statement.where(self.user_table.rec_date < rec_date_end)
        if text_filter is not None and len(text_filter)>0:
            statement = statement.where(or_(self.user_table.email.ilike(f"%{text_filter}%"),
                                            self.user_table.full_name.ilike(f"%{text_filter}%")))
        if offset > 0:
            statement = statement.offset(offset)
        query_results = await self.session.execute(statement)
        return [u[0] for u in query_results.unique()]


    async def add_oauth_account(self, user: UP, create_dict: Dict[str, Any]) -> UP:
        if self.oauth_account_table is None:
            raise NotImplementedError()

        await self.session.refresh(user)
        oauth_account = self.oauth_account_table(**create_dict)
        self.session.add(oauth_account)
        user.oauth_accounts.append(oauth_account)  # type: ignore
        self.session.add(user)

        await self.session.flush()

        return user

    async def update_oauth_account(
        self, user: UP, oauth_account: OAP, update_dict: Dict[str, Any]
    ) -> UP:
        if self.oauth_account_table is None:
            raise NotImplementedError()

        for key, value in update_dict.items():
            setattr(oauth_account, key, value)
        self.session.add(oauth_account)
        await self.session.flush()

        return user

    async def _get_user(self, statement: Select) -> Optional[UP]:
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()




async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield UserDatabase(session, User, OAuthAccount)

async def get_access_token_db(session: AsyncSession = Depends(get_db),):  
    yield TokenDatabase(session, AccessToken)

def get_auth_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=int(3600*float(os.environ['AUTH_LIFETIME_HOURS'])))
