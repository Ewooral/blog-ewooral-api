import reflex as rx
from app.states.articles_state import ArticleState
from app.components.article_card import article_card


@rx.page(
    route="/articles",
    title="Articles",
    on_load=ArticleState.fetch_articles_and_categories,
)
def articles_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("AI & ML Research Articles", class_name="text-4xl font-bold mb-6"),
        rx.el.div(
            rx.el.input(
                placeholder="Search articles...",
                on_change=ArticleState.set_search_query.debounce(300),
                class_name="p-2 border rounded w-full md:w-1/2",
            ),
            rx.el.select(
                rx.el.option("All Categories", value=""),
                rx.foreach(
                    ArticleState.categories,
                    lambda category: rx.el.option(
                        category["name"], value=category["name"]
                    ),
                ),
                on_change=ArticleState.set_selected_category,
                class_name="p-2 border rounded",
            ),
            class_name="flex flex-col md:flex-row gap-4 mb-6",
        ),
        rx.cond(
            ArticleState.is_loading,
            rx.el.div(
                rx.el.p("Loading articles..."), rx.el.p(class_name="animate-spin")
            ),
            rx.el.div(
                rx.foreach(ArticleState.articles, article_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
        ),
        class_name="container mx-auto p-4",
    )