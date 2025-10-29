import reflex as rx


def index() -> rx.Component:
    """The home page of the app."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("book-open-check", class_name="h-12 w-12 text-blue-600"),
                rx.el.h1(
                    "Welcome to the AI & ML Research Blog",
                    class_name="mt-6 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl",
                ),
                rx.el.p(
                    "Your central hub for the latest in artificial intelligence and machine learning research. Discover articles, insights, and breakthroughs from leading experts.",
                    class_name="mt-6 text-lg leading-8 text-gray-600",
                ),
                rx.el.div(
                    rx.el.a(
                        "Browse Articles",
                        href="/articles",
                        class_name="rounded-md bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600",
                    ),
                    rx.el.a(
                        "API Docs",
                        href="/api/v1/docs",
                        class_name="text-sm font-semibold leading-6 text-gray-900",
                        is_external=True,
                    ),
                    class_name="mt-10 flex items-center justify-center gap-x-6",
                ),
                class_name="max-w-2xl text-center",
            ),
            class_name="flex-1 flex flex-col items-center justify-center px-6 py-24 sm:py-32 lg:px-8",
        ),
        class_name="min-h-screen bg-white flex flex-col font-['Inter']",
    )