from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from app.core.config import get_settings

settings = get_settings()

DATABASE_URL = "sqlite:///./library.db"

engine = create_engine(DATABASE_URL, echo=settings.debug, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Session:
    with SessionLocal() as session:
        yield session


def init_db():
    Base.metadata.create_all(bind=engine)
