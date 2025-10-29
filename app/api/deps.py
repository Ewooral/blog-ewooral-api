from typing import Generator
from sqlmodel import Session
from app.db.session import get_session as get_db_session


def get_session() -> Generator:
    yield from get_db_session()