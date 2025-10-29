from sqlmodel import create_engine, Session
import os
from urllib.parse import quote_plus

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "host")
DB_NAME = os.getenv("DB_NAME", "dbname")
DATABASE_URL = os.getenv(
    "REFLEX_DB_URL",
    f"postgresql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}",
)
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session