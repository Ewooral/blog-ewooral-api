import reflex as rx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.api.deps import get_session
from app.models.article import (
    Article,
    ArticleCreate,
    ArticleRead,
    ArticleReadWithDetails,
    ArticleUpdate,
)
from app.models.author import Author
from app.models.category import Category

router = APIRouter()


@router.post(
    "/",
    response_model=ArticleRead,
    status_code=201,
    summary="Create a new article (requires authentication)",
)
def create_article(
    *, session: Session = Depends(get_session), article_in: ArticleCreate
) -> Article:
    """
    Create a new article with an author and category.
    """
    author = session.get(Author, article_in.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    category = session.get(Category, article_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db_article = Article.model_validate(article_in)
    session.add(db_article)
    session.commit()
    session.refresh(db_article)
    return db_article


@router.get(
    "/", response_model=list[ArticleReadWithDetails], summary="List all articles"
)
def read_articles(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    category: str | None = None,
    tags: str | None = Query(
        default=None, description="Comma-separated tag names to filter by"
    ),
    search: str | None = None,
) -> list[Article]:
    """
    Retrieve articles with optional filtering by category, tags, and full-text search.
    """
    query = select(Article).join(Author).join(Category)
    if category:
        query = query.where(Category.name == category)
    if tags:
        tag_names = [tag.strip() for tag in tags.split(",")]
        from app.models.tag import Tag, ArticleTagLink

        query = query.join(ArticleTagLink).join(Tag).where(Tag.name.in_(tag_names))
    if search:
        search_term = f"%{search}%"
        query = query.where(
            Article.title.ilike(search_term) | Article.content.ilike(search_term)
        )
    articles = session.exec(query.offset(offset).limit(limit).distinct()).all()
    return articles


@router.get(
    "/{article_id}",
    response_model=ArticleReadWithDetails,
    summary="Get a specific article",
)
def read_article(
    *, session: Session = Depends(get_session), article_id: int
) -> Article:
    """
    Get an article by its ID.
    """
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.patch(
    "/{article_id}",
    response_model=ArticleRead,
    summary="Update an article (requires authentication)",
)
def update_article(
    *,
    session: Session = Depends(get_session),
    article_id: int,
    article_in: ArticleUpdate,
) -> Article:
    """
    Update an article's title, content, or category.
    """
    db_article = session.get(Article, article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article_in.category_id:
        category = session.get(Category, article_in.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    update_data = article_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_article, key, value)
    session.add(db_article)
    session.commit()
    session.refresh(db_article)
    return db_article


@router.delete(
    "/{article_id}",
    status_code=204,
    summary="Delete an article (requires authentication)",
)
def delete_article(*, session: Session = Depends(get_session), article_id: int):
    """
    Delete an article by its ID.
    """
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    session.delete(article)
    session.commit()
    return