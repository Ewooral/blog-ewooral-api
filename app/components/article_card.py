import reflex as rx
from app.states.articles_state import Article


def article_card(article: Article) -> rx.Component:
    return rx.el.div(
        rx.el.h3(article["title"], class_name="text-xl font-bold mb-2"),
        rx.el.p(
            "By ",
            article["author"]["name"],
            " in ",
            rx.el.span(
                article["category"]["name"], class_name="font-semibold text-blue-600"
            ),
        ),
        rx.el.p(
            article["content"].to_string()[0:150] + "...",
            class_name="mt-2 text-gray-600",
        ),
        rx.el.div(
            rx.foreach(
                article["tags"],
                lambda tag: rx.el.span(
                    tag["name"],
                    class_name="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2",
                ),
            ),
            class_name="mt-4",
        ),
        class_name="border p-4 rounded-lg shadow-md bg-white",
    )