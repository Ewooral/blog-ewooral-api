from sqlmodel import create_engine, Session
from urllib.parse import quote_plus

password = quote_plus("OWusu123@#")
DATABASE_URL = f"postgresql://strategyforge_user:{password}@62.171.135.105/bfam_backend"
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session