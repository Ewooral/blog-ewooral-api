import reflex as rx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import create_db_and_tables, create_initial_data
from app.pages.articles import articles_page


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    create_db_and_tables()
    create_initial_data()
    print("Database initialized successfully!")
    yield


fastapi_app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
fastapi_app.include_router(api_router, prefix=settings.API_V1_STR)


class State(rx.State):
    """The app state."""

    pass


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1(
                "Welcome to the AI & ML Research Blog",
                class_name="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-6",
            ),
            rx.el.p(
                "Explore the latest research, trends, and discussions in Artificial Intelligence and Machine Learning.",
                class_name="text-lg text-gray-600 mb-10 max-w-2xl text-center",
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        "Explore Articles",
                        rx.icon("arrow-right", class_name="ml-2"),
                        class_name="bg-blue-600 text-white px-8 py-4 rounded-lg shadow-lg hover:bg-blue-700 transition-all flex items-center font-semibold text-lg",
                    ),
                    href="/articles",
                ),
                rx.el.a(
                    rx.el.button(
                        "View API Docs",
                        rx.icon("book-open", class_name="ml-2"),
                        class_name="bg-gray-700 text-white px-8 py-4 rounded-lg shadow-lg hover:bg-gray-800 transition-all flex items-center font-semibold text-lg",
                    ),
                    href="/docs",
                    target="_blank",
                ),
                class_name="flex flex-col sm:flex-row gap-6",
            ),
            class_name="flex flex-col items-center justify-center text-center min-h-screen bg-gray-50 p-6",
        ),
        class_name="font-['Lato'] bg-white",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
            rel="stylesheet",
        ),
    ],
    api_transformer=fastapi_app,
)
app.add_page(index, route="/")
app.add_page(articles_page, route="/articles")