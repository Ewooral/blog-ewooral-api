import reflex as rx
from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class CategoryBase(SQLModel):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None


class Category(CategoryBase, table=True):
    id: UUID = Field(
        default_factory=uuid4, primary_key=True, index=True, nullable=False
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: UUID


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None