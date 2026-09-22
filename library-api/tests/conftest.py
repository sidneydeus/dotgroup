import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import Base, get_db

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


@pytest.fixture(autouse=True)
def setup_db():
    init_test_db()
    yield
    drop_test_db()


@pytest.fixture
def client() -> TestClient:
    def override_get_db():
        with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
