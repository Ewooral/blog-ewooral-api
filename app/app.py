import reflex as rx
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import create_db_and_tables, create_initial_data
from app.pages import articles


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    create_db_and_tables()
    create_initial_data()
    print("Database initialization complete.")
    yield


@rx.page(route="/", title="Home")
def index() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Welcome to the AI & ML Research Blog"),
        rx.el.p(
            "Navigate to the ",
            rx.el.a("Articles page", href="/articles"),
            " to see the content.",
        ),
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.api = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)
app.api.include_router(api_router, prefix=settings.API_V1_STR)
app.add_page(index)
app.add_page(articles.articles_page, route="/articles")