import reflex as rx
from typing import Optional
from sqlmodel import Field, SQLModel


class CategoryBase(SQLModel):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None