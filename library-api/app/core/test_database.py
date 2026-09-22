from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=test_engine, class_=Session, expire_on_commit=False)


def init_test_db():
    Base.metadata.create_all(bind=test_engine)


def drop_test_db():
    Base.metadata.drop_all(bind=test_engine)


def get_test_db() -> Session:
    with TestSessionLocal() as session:
        yield session
