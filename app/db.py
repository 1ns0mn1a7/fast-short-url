from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = "postgresql://admin@localhost:5432/url_shortener"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
