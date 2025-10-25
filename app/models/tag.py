import reflex as rx
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4


class ArticleTagLink(SQLModel, table=True):
    article_id: UUID | None = Field(
        default=None, foreign_key="article.id", primary_key=True
    )
    tag_id: UUID | None = Field(default=None, foreign_key="tag.id", primary_key=True)


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