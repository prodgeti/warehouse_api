import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from dotenv import load_dotenv

from database import get_db
from models import Base
from main import app

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

TEST_DB_NAME = "test_" + os.getenv("DB_NAME")
TEST_DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{TEST_DB_NAME}"

engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(TEST_DATABASE_URL)
)


def create_test_database():
    """Создание тестовой базы данных"""
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {TEST_DB_NAME}"))


def drop_test_database():
    """Удаление тестовой базы данных"""
    with engine.connect() as conn:

        conn.execute(text(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{TEST_DB_NAME}'
            AND pid <> pg_backend_pid();
        """))
        conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Создает тестовую базу данных перед тестами и удаляет её после"""
    create_test_database()
    yield
    drop_test_database()


@pytest.fixture(scope="module")
def db():
    test_engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
