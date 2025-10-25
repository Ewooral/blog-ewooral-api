import reflex as rx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from app.api.deps import get_session
from app.models.author import (
    Author,
    AuthorCreate,
    AuthorRead,
    AuthorUpdate,
    AuthorReadWithArticles,
)

router = APIRouter()


@router.post(
    "/", response_model=AuthorRead, status_code=201, summary="Create a new author"
)
def create_author(
    *, session: Session = Depends(get_session), author_in: AuthorCreate
) -> Author:
    """
    Create a new author.
    """
    db_author = Author.model_validate(author_in)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.get("/", response_model=list[AuthorRead], summary="List all authors")
def read_authors(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[Author]:
    """
    Retrieve a list of all authors.
    """
    authors = session.exec(select(Author).offset(offset).limit(limit)).all()
    return authors


@router.get(
    "/{author_id}",
    response_model=AuthorReadWithArticles,
    summary="Get a specific author",
)
def read_author(*, session: Session = Depends(get_session), author_id: UUID) -> Author:
    """
    Get an author by their ID, including their articles.
    """
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.patch("/{author_id}", response_model=AuthorRead, summary="Update an author")
def update_author(
    *, session: Session = Depends(get_session), author_id: UUID, author_in: AuthorUpdate
) -> Author:
    """
    Update an author's name or bio.
    """
    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    update_data = author_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_author, key, value)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.delete("/{author_id}", status_code=204, summary="Delete an author")
def delete_author(*, session: Session = Depends(get_session), author_id: UUID):
    """
    Delete an author.
    """
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return