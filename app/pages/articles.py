import reflex as rx
from app.states.articles_state import ArticlesState
from app.components.article_card import article_card


def articles_page_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "AI & ML Research Blog",
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Exploring the frontiers of Artificial Intelligence and Machine Learning.",
                    class_name="text-gray-600 mt-2",
                ),
                class_name="max-w-2xl",
            ),
            class_name="w-full max-w-5xl mx-auto px-4 py-8",
        ),
        class_name="bg-gray-50 border-b border-gray-200",
    )


def articles_filters() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="h-5 w-5 text-gray-400"),
                    class_name="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none",
                ),
                rx.el.input(
                    placeholder="Search articles...",
                    on_change=ArticlesState.set_search_query,
                    class_name="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500",
                ),
                class_name="relative w-full max-w-sm",
            ),
            rx.el.select(
                rx.el.option("All Categories", value=""),
                rx.foreach(
                    ArticlesState.categories,
                    lambda c: rx.el.option(c["name"], value=c["name"]),
                ),
                on_change=ArticlesState.set_selected_category,
                value=ArticlesState.selected_category,
                class_name="border border-gray-300 rounded-lg px-4 py-2 focus:ring-blue-500 focus:border-blue-500",
            ),
            class_name="flex flex-wrap items-center gap-4",
        ),
        class_name="w-full max-w-5xl mx-auto px-4 py-6",
    )


def articles_list() -> rx.Component:
    return rx.el.div(
        rx.cond(
            ArticlesState.is_loading,
            rx.el.div(
                rx.foreach(
                    [1, 2, 3, 4],
                    lambda i: rx.el.div(
                        rx.el.div(class_name="h-4 bg-gray-200 rounded w-3/4 mb-2"),
                        rx.el.div(class_name="h-3 bg-gray-200 rounded w-1/2 mb-4"),
                        rx.el.div(class_name="h-20 bg-gray-200 rounded"),
                        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm animate-pulse",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            rx.el.div(
                rx.foreach(ArticlesState.articles, article_card),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
        ),
        rx.cond(
            ~ArticlesState.is_loading & (ArticlesState.articles.length() == 0),
            rx.el.div(
                rx.icon("search-x", class_name="h-12 w-12 text-gray-400 mx-auto"),
                rx.el.h3(
                    "No Articles Found",
                    class_name="mt-4 text-lg font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Try adjusting your search or filter criteria.",
                    class_name="mt-1 text-gray-600",
                ),
                class_name="text-center py-16",
            ),
            None,
        ),
        class_name="w-full max-w-5xl mx-auto px-4",
    )


def articles() -> rx.Component:
    """The main page for displaying articles."""
    return rx.el.main(
        articles_page_header(),
        articles_filters(),
        articles_list(),
        on_mount=ArticlesState.fetch_articles_and_categories,
        class_name="bg-gray-50 min-h-screen font-['Inter']",
    )