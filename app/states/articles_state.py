import reflex as rx
from typing import TypedDict, Any
import httpx
import logging

API_URL = "http://127.0.0.1:8000/api/v1"


class AuthorDict(TypedDict):
    id: str
    name: str
    bio: str | None


class CategoryDict(TypedDict):
    id: str
    name: str
    description: str | None


class ArticleDict(TypedDict):
    id: str
    title: str
    content: str
    published_at: str | None
    author_id: str
    category_id: str
    author: AuthorDict
    category: CategoryDict
    tags: list


class ArticleState(rx.State):
    articles: list[ArticleDict] = []
    categories: list[CategoryDict] = []
    search_query: str = ""
    selected_category: str = "all"
    is_loading: bool = True

    @rx.event(background=True)
    async def fetch_articles_and_categories(self):
        async with self:
            self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                params = {}
                if self.selected_category != "all":
                    params["category"] = self.selected_category
                if self.search_query:
                    params["search"] = self.search_query
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
    def set_selected_category(self, category_name: str):
        self.selected_category = category_name
        return ArticleState.fetch_articles_and_categories