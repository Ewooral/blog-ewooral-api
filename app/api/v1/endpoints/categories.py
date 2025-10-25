import reflex as rx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from uuid import UUID
from app.api.deps import get_session
from app.models.category import Category, CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter()


@router.post(
    "/", response_model=CategoryRead, status_code=201, summary="Create a new category"
)
def create_category(
    *, session: Session = Depends(get_session), category_in: CategoryCreate
) -> Category:
    """
    Create a new category for articles.
    """
    existing_category = session.exec(
        select(Category).where(Category.name == category_in.name)
    ).first()
    if existing_category:
        raise HTTPException(
            status_code=409, detail="Category with this name already exists"
        )
    db_category = Category.model_validate(category_in)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.get("/", response_model=list[CategoryRead], summary="List all categories")
def read_categories(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=50, le=100),
) -> list[Category]:
    """
    Retrieve a list of all available categories.
    """
    categories = session.exec(select(Category).offset(offset).limit(limit)).all()
    return categories


@router.get(
    "/{category_id}", response_model=CategoryRead, summary="Get a specific category"
)
def read_category(
    *, session: Session = Depends(get_session), category_id: UUID
) -> Category:
    """
    Get a category by its ID.
    """
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch(
    "/{category_id}", response_model=CategoryRead, summary="Update a category"
)
def update_category(
    *,
    session: Session = Depends(get_session),
    category_id: UUID,
    category_in: CategoryUpdate,
) -> Category:
    """
    Update a category's name or description.
    """
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category_in.name:
        existing = session.exec(
            select(Category).where(Category.name == category_in.name)
        ).first()
        if existing and existing.id != category_id:
            raise HTTPException(
                status_code=409, detail="Another category with this name already exists"
            )
    update_data = category_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=204, summary="Delete a category")
def delete_category(*, session: Session = Depends(get_session), category_id: UUID):
    """
    Delete a category.
    """
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return