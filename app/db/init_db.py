import reflex as rx
from sqlmodel import SQLModel, Session, select
from app.db.session import engine
from app.models.author import Author
from app.models.category import Category
from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User, Role
from app.core.security import get_password_hash
from datetime import datetime


def create_db_and_tables():
    from app.models import user, article, author, category, tag, link

    SQLModel.metadata.create_all(engine)


def create_initial_data():
    with Session(engine) as session:
        if not session.exec(select(User)).first():
            print("Creating initial user data...")
            user_admin = User(
                email="admin@aimlblog.com",
                hashed_password=get_password_hash("AdminPass123!"),
                role=Role.ADMIN,
                is_active=True,
            )
            user_author = User(
                email="author@aimlblog.com",
                hashed_password=get_password_hash("AuthorPass123!"),
                role=Role.AUTHOR,
                is_active=True,
            )
            user_reader = User(
                email="reader@aimlblog.com",
                hashed_password=get_password_hash("ReaderPass123!"),
                role=Role.READER,
                is_active=True,
            )
            session.add_all([user_admin, user_author, user_reader])
            session.commit()
            print("Initial users created.")
        if not session.exec(select(Author)).first():
            print("Creating initial blog data...")
            author1 = Author(
                name="Dr. Ada Lovelace",
                bio="Pioneering computer scientist and mathematician.",
            )
            author2 = Author(
                name="Dr. Alan Turing",
                bio="Father of theoretical computer science and artificial intelligence.",
            )
            session.add(author1)
            session.add(author2)
            session.commit()
            session.refresh(author1)
            session.refresh(author2)
            cat1 = Category(
                name="Machine Learning",
                description="Articles about ML algorithms, models, and techniques.",
            )
            cat2 = Category(
                name="Natural Language Processing",
                description="Exploring how computers process and understand human language.",
            )
            session.add(cat1)
            session.add(cat2)
            session.commit()
            session.refresh(cat1)
            session.refresh(cat2)
            article1 = Article(
                title="The Future of Neural Networks",
                content="Deep learning continues to evolve...",
                author_id=author1.id,
                category_id=cat1.id,
                published_at=datetime.utcnow(),
            )
            article2 = Article(
                title="Understanding Transformer Models",
                content="Transformers have revolutionized NLP...",
                author_id=author2.id,
                category_id=cat2.id,
                published_at=datetime.utcnow(),
            )
            session.add(article1)
            session.add(article2)
            session.commit()
            print("Initial blog data created.")