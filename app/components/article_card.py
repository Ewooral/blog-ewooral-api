import reflex as rx
from app.models.article import ArticleReadWithDetails


def article_card(article: ArticleReadWithDetails) -> rx.Component:
    """Component to display a single article card."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.h3(
                        article["title"],
                        class_name="text-lg font-bold text-gray-900 leading-tight",
                    ),
                    href=f"/articles/{article['id']}",
                    class_name="hover:underline",
                ),
                rx.el.p(
                    f"By {article['author']['name']}",
                    class_name="text-sm text-gray-600 mt-1",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.span(
                    article["category"]["name"],
                    class_name="text-xs font-semibold text-blue-800 bg-blue-100 rounded-full px-3 py-1",
                ),
                class_name="w-fit",
            ),
            class_name="flex items-start justify-between gap-4",
        ),
        rx.el.p(
            f"{article['content'].to_string()[:150]}...",
            class_name="text-gray-700 mt-2 text-sm leading-relaxed",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    article["tags"],
                    lambda tag: rx.el.span(
                        tag["name"],
                        class_name="text-xs text-gray-500 bg-gray-100 rounded-full px-2 py-1",
                    ),
                ),
                class_name="flex flex-wrap gap-2",
            ),
            rx.el.a(
                "Read More",
                href=f"/articles/{article['id']}",
                class_name="text-sm font-semibold text-blue-600 hover:text-blue-800",
            ),
            class_name="flex items-center justify-between mt-4",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow duration-300",
    )