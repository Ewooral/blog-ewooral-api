import reflex as rx
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import create_db_and_tables, create_initial_data
from app.pages import index, articles

fastapi_app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)
if settings.BACKEND_CORS_ORIGINS:
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@fastapi_app.on_event("startup")
def on_startup():
    create_db_and_tables()
    create_initial_data()


fastapi_app.include_router(api_router, prefix=settings.API_V1_STR)
app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        )
    ],
)
app.add_page(index.index, route="/")
app.add_page(articles.articles, route="/articles")
app.api = fastapi_app