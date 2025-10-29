import reflex as rx
import httpx
from app.models.article import ArticleReadWithDetails
from app.models.category import CategoryRead
import logging


class ArticlesState(rx.State):
    """State to manage fetching and filtering articles."""

    articles: list[ArticleReadWithDetails] = []
    categories: list[CategoryRead] = []
    is_loading: bool = True
    search_query: str = ""
    selected_category: str = ""

    @rx.event(background=True)
    async def fetch_articles_and_categories(self):
        """Fetch articles and categories from the FastAPI backend."""
        async with self:
            self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                params = {}
                if self.search_query:
                    params["search"] = self.search_query
                if self.selected_category:
                    params["category"] = self.selected_category
                articles_response = await client.get(
                    f"http://localhost:8000/api/v1/articles", params=params
                )
                articles_response.raise_for_status()
                articles_data = articles_response.json()
                categories_response = await client.get(
                    f"http://localhost:8000/api/v1/categories"
                )
                categories_response.raise_for_status()
                categories_data = categories_response.json()
                async with self:
                    self.articles = articles_data
                    self.categories = categories_data
        except httpx.HTTPStatusError as e:
            logging.exception(
                f"HTTP error fetching data: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        return ArticlesState.fetch_articles_and_categories

    @rx.event
    def set_selected_category(self, category: str):
        self.selected_category = category
        return ArticlesState.fetch_articles_and_categories