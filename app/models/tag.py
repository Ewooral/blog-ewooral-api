import reflex as rx
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.article import Article, ArticleRead
from app.models.link import ArticleTagLink


class TagBase(SQLModel):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    articles: list["Article"] = Relationship(
        back_populates="tags", link_model=ArticleTagLink
    )


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int


class TagUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TagReadWithArticles(TagRead):
    articles: list["ArticleRead"] = []