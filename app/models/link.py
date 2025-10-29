from sqlmodel import Field, SQLModel
from typing import Optional


class ArticleTagLink(SQLModel, table=True):
    article_id: Optional[int] = Field(
        default=None, foreign_key="article.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)