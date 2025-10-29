import reflex as rx
import httpx
import logging
from typing import TypedDict, Optional


class Author(TypedDict):
    id: int
    name: str
    bio: Optional[str]


class Category(TypedDict):
    id: int
    name: str
    description: Optional[str]


class Tag(TypedDict):
    id: int
    name: str
    description: Optional[str]


class Article(TypedDict):
    id: int
    title: str
    content: str
    published_at: str
    author_id: int
    category_id: int
    author: Author
    category: Category
    tags: list[Tag]


API_URL = "http://localhost:8000/api/v1"


class ArticleState(rx.State):
    articles: list[Article] = []
    categories: list[Category] = []
    is_loading: bool = False
    search_query: str = ""
    selected_category: str = ""

    @rx.event(background=True)
    async def fetch_articles_and_categories(self):
        async with self:
            self.is_loading = True
        try:
            params = {}
            if self.search_query:
                params["search"] = self.search_query
            if self.selected_category:
                params["category"] = self.selected_category
            async with httpx.AsyncClient() as client:
                articles_res = await client.get(f"{API_URL}/articles/", params=params)
                articles_res.raise_for_status()
                categories_res = await client.get(f"{API_URL}/categories/")
                categories_res.raise_for_status()
                async with self:
                    self.articles = articles_res.json()
                    self.categories = categories_res.json()
        except httpx.HTTPError as e:
            logging.exception(f"HTTP error occurred: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        return ArticleState.fetch_articles_and_categories

    @rx.event
    def set_selected_category(self, category: str):
        self.selected_category = category
        return ArticleState.fetch_articles_and_categories