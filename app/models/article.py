import reflex as rx
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
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
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=True
    )
    author_id: int = Field(foreign_key="author.id")
    category_id: int = Field(foreign_key="category.id")
    author: "Author" = Relationship(back_populates="articles")
    category: "Category" = Relationship()
    tags: list["Tag"] = Relationship(
        back_populates="articles", link_model=ArticleTagLink
    )


class ArticleCreate(ArticleBase):
    author_id: int
    category_id: int


class ArticleRead(ArticleBase):
    id: int
    author_id: int
    category_id: int


class ArticleReadWithDetails(ArticleRead):
    author: AuthorRead
    category: CategoryRead
    tags: list[TagRead] = []


class ArticleUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None