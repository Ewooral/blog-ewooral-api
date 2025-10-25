import reflex as rx
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    role: Role = Field(default=Role.READER)


class User(UserBase, table=True):
    id: UUID = Field(
        default_factory=uuid4, primary_key=True, index=True, nullable=False
    )
    hashed_password: str
    is_active: bool = Field(default=True)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    is_active: bool


class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[Role] = None