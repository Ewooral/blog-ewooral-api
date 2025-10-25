import reflex as rx
from app.states.articles_state import ArticleDict


def article_card(article: ArticleDict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    article["category"]["name"],
                    class_name="text-sm font-medium text-blue-600",
                ),
                class_name="mb-3",
            ),
            rx.el.h2(
                article["title"],
                class_name="text-xl font-semibold text-gray-900 mb-2 truncate",
            ),
            rx.el.p(
                f"{article['content'][:100]}...",
                class_name="text-gray-600 text-sm mb-4 h-10 overflow-hidden",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={article['author']['name']}",
                    class_name="w-8 h-8 rounded-full mr-3",
                ),
                rx.el.div(
                    rx.el.p(
                        article["author"]["name"],
                        class_name="text-sm font-semibold text-gray-800",
                    ),
                    rx.el.p(
                        rx.cond(
                            article["published_at"],
                            article["published_at"].to_string().split("T")[0],
                            "Not Published",
                        ),
                        class_name="text-xs text-gray-500",
                    ),
                ),
                class_name="flex items-center",
            )
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between hover:shadow-lg transition-shadow duration-300 h-full",
    )