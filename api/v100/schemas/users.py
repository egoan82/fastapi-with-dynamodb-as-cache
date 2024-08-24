from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CommonFields(BaseModel):
    name: str
    first_last_name: str
    second_last_name: Optional[str] = None
    email: EmailStr


class UserRead(CommonFields):
    id: UUID


class UserCreate(CommonFields):
    pass


class UserUpdate(CommonFields):
    pass


class UserDelete(BaseModel):
    id: UUID
