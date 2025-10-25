import reflex as rx
from app.states.articles_state import ArticleState
from app.components.article_card import article_card


def loading_skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="h-4 bg-gray-200 rounded w-1/4 mb-4"),
        rx.el.div(class_name="h-6 bg-gray-200 rounded w-3/4 mb-2"),
        rx.el.div(class_name="h-4 bg-gray-200 rounded w-full mb-4"),
        rx.el.div(class_name="h-4 bg-gray-200 rounded w-full mb-4"),
        rx.el.div(
            rx.el.div(class_name="w-8 h-8 bg-gray-200 rounded-full mr-3"),
            rx.el.div(
                rx.el.div(class_name="h-4 bg-gray-200 rounded w-24 mb-1"),
                rx.el.div(class_name="h-3 bg-gray-200 rounded w-20"),
                class_name="flex-1",
            ),
            class_name="flex items-center mt-auto",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 p-6 animate-pulse flex flex-col",
    )


def articles_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "AI & ML Research Articles",
                class_name="text-4xl font-bold text-gray-900",
            ),
            rx.el.p(
                "Discover the latest insights and breakthroughs.",
                class_name="text-lg text-gray-600 mt-2",
            ),
            class_name="text-center mb-12",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    placeholder="Search articles...",
                    on_change=ArticleState.set_search_query.debounce(300),
                    default_value=ArticleState.search_query,
                    class_name="w-full md:w-1/2 lg:w-1/3 px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition",
                ),
                rx.el.select(
                    rx.el.option("All Categories", value="all"),
                    rx.foreach(
                        ArticleState.categories,
                        lambda category: rx.el.option(
                            category["name"], value=category["name"]
                        ),
                    ),
                    value=ArticleState.selected_category,
                    on_change=ArticleState.set_selected_category,
                    class_name="px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 transition bg-white",
                ),
                class_name="flex flex-col md:flex-row gap-4 mb-8",
            ),
            rx.cond(
                ArticleState.is_loading,
                rx.el.div(
                    rx.foreach(range(6), lambda i: loading_skeleton()),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8",
                ),
                rx.el.div(
                    rx.foreach(ArticleState.articles, article_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8",
                ),
            ),
        ),
        on_mount=ArticleState.fetch_articles_and_categories,
        class_name="container mx-auto px-6 py-12 bg-gray-50 min-h-screen",
    )