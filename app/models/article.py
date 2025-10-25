import reflex as rx
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from app.models.author import AuthorRead
from app.models.category import CategoryRead
from app.models.tag import TagRead
from app.models.link import ArticleTagLink


class ArticleBase(SQLModel):
    title: str
    content: str
    published_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=True
    )


class Article(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4, primary_key=True, index=True, nullable=False
    )
    title: str
    content: str
    published_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=True
    )
    author_id: UUID = Field(foreign_key="author.id")
    category_id: UUID = Field(foreign_key="category.id")
    author: "Author" = Relationship(back_populates="articles")
    category: "Category" = Relationship()
    tags: list["Tag"] = Relationship(
        back_populates="articles", link_model=ArticleTagLink
    )


class ArticleCreate(ArticleBase):
    author_id: UUID
    category_id: UUID


class ArticleRead(ArticleBase):
    id: UUID
    author_id: UUID
    category_id: UUID


class ArticleReadWithDetails(ArticleRead):
    author: AuthorRead
    category: CategoryRead
    tags: list[TagRead] = []


class ArticleUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[UUID] = None