import reflex as rx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from app.api.deps import get_session
from app.models.tag import Tag, TagCreate, TagRead, TagUpdate, TagReadWithArticles

router = APIRouter()


@router.post("/", response_model=TagRead, status_code=201, summary="Create a new tag")
def create_tag(*, session: Session = Depends(get_session), tag_in: TagCreate) -> Tag:
    """
    Create a new tag.
    """
    existing_tag = session.exec(select(Tag).where(Tag.name == tag_in.name)).first()
    if existing_tag:
        raise HTTPException(status_code=409, detail="Tag with this name already exists")
    db_tag = Tag.from_orm(tag_in)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


@router.get("/", response_model=list[TagRead], summary="List all tags")
def read_tags(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[Tag]:
    """
    Retrieve a list of all tags.
    """
    tags = session.exec(select(Tag).offset(offset).limit(limit)).all()
    return tags


@router.get(
    "/{tag_id}", response_model=TagReadWithArticles, summary="Get a specific tag"
)
def read_tag(*, session: Session = Depends(get_session), tag_id: UUID) -> Tag:
    """
    Get a tag by its ID, including associated articles.
    """
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.patch("/{tag_id}", response_model=TagRead, summary="Update a tag")
def update_tag(
    *, session: Session = Depends(get_session), tag_id: UUID, tag_in: TagUpdate
) -> Tag:
    """
    Update a tag's name or description.
    """
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    update_data = tag_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag, key, value)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


@router.delete("/{tag_id}", status_code=204, summary="Delete a tag")
def delete_tag(*, session: Session = Depends(get_session), tag_id: UUID):
    """
    Delete a tag.
    """
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
    return