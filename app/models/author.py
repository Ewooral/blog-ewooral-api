from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.models.article import Article, ArticleRead


class AuthorBase(SQLModel):
    name: str = Field(index=True)
    bio: Optional[str] = Field(default=None)


class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    articles: list["Article"] = Relationship(back_populates="author")


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int


class AuthorReadWithArticles(AuthorRead):
    articles: list["ArticleRead"] = []


class AuthorUpdate(SQLModel):
    name: Optional[str] = None
    bio: Optional[str] = None