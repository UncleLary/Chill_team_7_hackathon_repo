import uuid
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
from pydantic import Field, BaseModel
from fastapi_users import schemas
from fastapi import Query


class UserRead(schemas.BaseUser[uuid.UUID]):
    full_name: Optional[str]
    profile_picture_url: Optional[str]
    is_profile_complete: bool
    rec_date: datetime

class UserListPage(BaseModel):
    content : List[UserRead]
    is_more_data_available : bool

@dataclass
class UserListFilter:
    is_active : Optional[bool] = Query(True)
    rec_date_start : Optional[datetime] = Query(None)
    rec_date_end : Optional[datetime] = Query(None)
    text_filter : Optional[str] = Query("", max_length=64)
    
class UserCreate(schemas.BaseUserCreate):
    full_name: Optional[str] = Field(min_length=2, max_length=75)
    profile_picture_url: Optional[str] = Field(max_length=200)

class UserCreateWithExtraArgs(schemas.BaseUserCreate):
    full_name: Optional[str] = Field(min_length=2, max_length=75)
    profile_picture_url: Optional[str] = Field(max_length=200)
    turnstile_token : str = Field(max_length=2048)
    invitation_token : Optional[uuid.UUID] = Field(None)

class UserUpdate(schemas.BaseUserUpdate):
    full_name: Optional[str] = Field(min_length=2, max_length=75)
    profile_picture_url: Optional[str] = Field(max_length=200)

class ForgotPasswordRequest(BaseModel):
    email : str = Field(min_length=5, max_length=320)
    turnstile_token : str = Field(max_length=2048)
