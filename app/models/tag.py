import reflex as rx
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from app.models.article import Article, ArticleRead
from app.models.link import ArticleTagLink


class TagBase(SQLModel):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None


class Tag(TagBase, table=True):
    id: UUID = Field(
        default_factory=uuid4, primary_key=True, index=True, nullable=False
    )
    articles: list["Article"] = Relationship(
        back_populates="tags", link_model=ArticleTagLink
    )


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: UUID


class TagUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TagReadWithArticles(TagRead):
    articles: list["ArticleRead"] = []