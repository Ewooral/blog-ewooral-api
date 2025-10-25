@rx.page(route="/api/articles")
def create_article(
    article_data: dict[str, str | UUID], session: Session = Depends(get_session)
):
    """Create a new article"""
    try:
        author = session.get(Author, article_data["author_id"])
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        category = session.get(Category, article_data["category_id"])
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        db_article = Article(
            title=article_data["title"],
            content=article_data["content"],
            author_id=article_data["author_id"],
            category_id=article_data["category_id"],
        )
        session.add(db_article)
        session.commit()
        session.refresh(db_article)
        return JSONResponse(
            {
                "id": str(db_article.id),
                "title": db_article.title,
                "content": db_article.content,
                "author_id": str(db_article.author_id),
                "category_id": str(db_article.category_id),
                "published_at": db_article.published_at.isoformat()
                if db_article.published_at
                else None,
            }
        )
    except Exception as e:
        logging.exception(f"Error creating article: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rx.page(route="/api/authors")
def get_authors(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 100
):
    """Get all authors"""
    try:
        authors = session.exec(select(Author).offset(offset).limit(limit)).all()
        result = []
        for author in authors:
            result.append(
                {"id": str(author.id), "name": author.name, "bio": author.bio}
            )
        return JSONResponse(result)
    except Exception as e:
        logging.exception(f"Error getting authors: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rx.page(route="/api/authors")
def create_author(author_data: dict[str, str], session: Session = Depends(get_session)):
    """Create a new author"""
    try:
        db_author = Author(name=author_data["name"], bio=author_data.get("bio"))
        session.add(db_author)
        session.commit()
        session.refresh(db_author)
        return JSONResponse(
            {"id": str(db_author.id), "name": db_author.name, "bio": db_author.bio}
        )
    except Exception as e:
        logging.exception(f"Error creating author: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rx.page(route="/api/categories")
def get_categories(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 50
):
    """Get all categories"""
    try:
        categories = session.exec(select(Category).offset(offset).limit(limit)).all()
        result = []
        for category in categories:
            result.append(
                {
                    "id": str(category.id),
                    "name": category.name,
                    "description": category.description,
                }
            )
        return JSONResponse(result)
    except Exception as e:
        logging.exception(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rx.page(route="/api/categories")
def create_category(
    category_data: dict[str, str], session: Session = Depends(get_session)
):
    """Create a new category"""
    try:
        existing = session.exec(
            select(Category).where(Category.name == category_data["name"])
        ).first()
        if existing:
            raise HTTPException(
                status_code=409, detail="Category with this name already exists"
            )
        db_category = Category(
            name=category_data["name"], description=category_data.get("description")
        )
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return JSONResponse(
            {
                "id": str(db_category.id),
                "name": db_category.name,
                "description": db_category.description,
            }
        )
    except Exception as e:
        if "409" in str(e):
            raise e
        logging.exception(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@rx.page(route="/api/tags")
def get_tags(
    session: Session = Depends(get_session), offset: int = 0, limit: int = 100
):
    """Get all tags"""
    try:
        tags = session.exec(select(Tag).offset(offset).limit(limit)).all()
        result = []
        for tag in tags:
            result.append(
                {"id": str(tag.id), "name": tag.name, "description": tag.description}
            )
        return JSONResponse(result)
    except Exception as e:
        logging.exception(f"Error getting tags: {e}")
        raise HTTPException(status_code=500, detail=str(e))