import reflex as rx
from sqlmodel import Field, SQLModel
from uuid import UUID


class ArticleTagLink(SQLModel, table=True):
    article_id: UUID | None = Field(
        default=None, foreign_key="article.id", primary_key=True
    )
    tag_id: UUID | None = Field(default=None, foreign_key="tag.id", primary_key=True)