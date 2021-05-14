"""
Style for the pydantic models taken from FastAPI
creator tiangolo's project template in Github
https://tinyurl.com/3esb4r2j

Modified for my use
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import UUID4

from .token import Token


# Shared properties
class UserBase(BaseModel):
    username: str = Field(..., max_length=150)


class User(BaseModel):
    user_uid: UUID4
    username: str = Field(..., max_length=150)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


class UserDBBase(User):
    email: Optional[EmailStr] = Field(None, exclusiveMaximum=255)
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


# Additional properties stored in DB
class UserInDB(UserDBBase):
    password: str
