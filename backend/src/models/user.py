from datetime import datetime
from typing import List
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql import false
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
)
from core.database import Base

class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass

class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):  
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    is_profile_complete: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=false())
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )
    profile_picture_url: Mapped[str] = mapped_column(String(200), nullable=True)
    full_name: Mapped[str] = mapped_column(String(75), nullable=True)
    rec_date: Mapped[datetime] = mapped_column(DateTime(), nullable=False, server_default=func.now())
