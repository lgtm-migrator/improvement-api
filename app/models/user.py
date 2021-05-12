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


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str = Field(..., max_length=150)
    password: str
    email: Optional[EmailStr] = Field(None, exclusiveMaximum=255)


class UserInDBBase(UserBase):
    user_uid: UUID4


class UserWithToken(UserInDBBase):
    token_data: Token


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    email: Optional[EmailStr] = Field(None, exclusiveMaximum=255)
    is_active: bool = True
    password: str
    created_at: datetime
    updated_at: datetime
