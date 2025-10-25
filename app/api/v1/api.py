import reflex as rx
from fastapi import APIRouter
from app.api.v1.endpoints import articles, categories, authors, tags, users, login

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(authors.router, prefix="/authors", tags=["authors"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])