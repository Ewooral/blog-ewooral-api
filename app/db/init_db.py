import reflex as rx
from sqlmodel import SQLModel, Session, select
from app.db.session import engine
from app.models.author import Author
from app.models.category import Category
from app.models.article import Article
from app.models.tag import Tag
from app.models.user import User, Role, Permission
from app.core.security import get_password_hash
from datetime import datetime


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_initial_data():
    with Session(engine) as session:
        if not session.exec(select(User)).first():
            print("Creating initial user and RBAC data...")
            perm_create = Permission(
                name="create_articles", description="Create new articles"
            )
            perm_edit = Permission(
                name="edit_articles", description="Edit own articles"
            )
            perm_delete = Permission(
                name="delete_articles", description="Delete own articles"
            )
            perm_admin_read = Permission(
                name="admin_read", description="Read admin dashboard"
            )
            role_admin = Role(
                name="admin",
                description="Administrator",
                permissions=[perm_admin_read, perm_create, perm_edit, perm_delete],
            )
            role_author = Role(
                name="author",
                description="Article Author",
                permissions=[perm_create, perm_edit, perm_delete],
            )
            role_reader = Role(name="reader", description="Regular Reader")
            user_admin = User(
                email="admin@aimlblog.com",
                hashed_password=get_password_hash("AdminPass123!"),
                is_active=True,
                is_admin=True,
                roles=[role_admin],
            )
            user_author = User(
                email="author@aimlblog.com",
                hashed_password=get_password_hash("AuthorPass123!"),
                is_active=True,
                roles=[role_author],
            )
            user_reader = User(
                email="reader@aimlblog.com",
                hashed_password=get_password_hash("ReaderPass123!"),
                is_active=True,
                roles=[role_reader],
            )
            session.add_all(
                [
                    user_admin,
                    user_author,
                    user_reader,
                    role_admin,
                    role_author,
                    role_reader,
                    perm_create,
                    perm_edit,
                    perm_delete,
                    perm_admin_read,
                ]
            )
            session.commit()
            print("Initial users and RBAC created.")
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
            session.add_all([author1, author2])
            session.commit()
            cat1 = Category(
                name="Machine Learning",
                description="Articles about ML algorithms, models, and techniques.",
            )
            cat2 = Category(
                name="Natural Language Processing",
                description="Exploring how computers process and understand human language.",
            )
            session.add_all([cat1, cat2])
            session.commit()
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
            session.add_all([article1, article2])
            session.commit()
            print("Initial blog data created.")