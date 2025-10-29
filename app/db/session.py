import reflex as rx
from sqlmodel import create_engine, Session

DATABASE_URL = "postgresql://strategyforge_user:OWusu123@#@62.171.135.105/bfam_backend"
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session