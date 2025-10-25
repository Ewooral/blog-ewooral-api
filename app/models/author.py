import reflex as rx
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from app.models.article import Article, ArticleRead


class AuthorBase(SQLModel):
    name: str = Field(index=True)
    bio: Optional[str] = Field(default=None)


class Author(AuthorBase, table=True):
    id: UUID = Field(
        default_factory=uuid4, primary_key=True, index=True, nullable=False
    )
    articles: list["Article"] = Relationship(back_populates="author")


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: UUID


class AuthorReadWithArticles(AuthorRead):
    articles: list["ArticleRead"] = []


class AuthorUpdate(SQLModel):
    name: Optional[str] = None
    bio: Optional[str] = None