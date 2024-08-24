from typing import Optional
import uuid

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: uuid.UUID = Field(
        default=uuid.uuid4(),
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str
    first_last_name: str
    second_last_name: Optional[str] = None
    email: str

    __tablename__ = 'users'
