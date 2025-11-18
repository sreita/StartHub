import pytest
from fastapi.testclient import TestClient
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.main import app
from backend.db.base import Base
from backend.db.session import get_db


@pytest.fixture(scope="session")
def test_engine():
    # Shared in-memory SQLite for tests
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Minimal tables for FKs in same metadata (guard against redefinition)
    if "User" not in Base.metadata.tables:
        Table(
            "User",
            Base.metadata,
            Column("user_id", Integer, primary_key=True, autoincrement=True),
            Column("email", String),
            Column("password_hash", String),
            Column("first_name", String),
            Column("last_name", String),
            Column("is_enabled", Boolean),
        )
    if "Category" not in Base.metadata.tables:
        Table(
            "Category",
            Base.metadata,
            Column("category_id", Integer, primary_key=True, autoincrement=True),
            Column("name", String),
        )
    if "Startup" not in Base.metadata.tables:
        Table(
            "Startup",
            Base.metadata,
            Column("startup_id", Integer, primary_key=True, autoincrement=True),
            Column("name", String),
            Column("description", String),
            Column("owner_user_id", Integer),
            Column("category_id", Integer),
        )

    Base.metadata.create_all(bind=engine)

    # Seed: two users, one category, one startup
    with engine.begin() as conn:
        conn.exec_driver_sql("INSERT INTO Category (name) VALUES ('General');")
        conn.exec_driver_sql(
            "INSERT INTO `User` (email, password_hash, first_name, last_name, is_enabled) VALUES ("
            "'tester1@example.com','hash','Tester','One',1);"
        )
        conn.exec_driver_sql(
            "INSERT INTO `User` (email, password_hash, first_name, last_name, is_enabled) VALUES ("
            "'tester2@example.com','hash','Tester','Two',1);"
        )
        conn.exec_driver_sql(
            "INSERT INTO Startup (name, description, owner_user_id, category_id) VALUES ("
            "'Demo','Desc',1,1);"
        )
    return engine


@pytest.fixture()
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def override_dependency(db_session):
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture()
def client():
    return TestClient(app)


def test_create_comment_user_not_found(client):
    resp = client.post(
        "/comments",
        params={"user_id": 999},
        json={"content": "Hola", "startup_id": 1},
    )
    assert resp.status_code == 404


def test_create_comment_startup_not_found(client):
    resp = client.post(
        "/comments",
        params={"user_id": 1},
        json={"content": "Hola", "startup_id": 999},
    )
    assert resp.status_code == 404


def test_comment_update_forbidden_other_user(client):
    # Create with user 1
    created = client.post(
        "/comments",
        params={"user_id": 1},
        json={"content": "Propio", "startup_id": 1},
    )
    assert created.status_code == 201, created.text
    cid = created.json()["comment_id"]

    # Try to update with user 2 (exists) → 403
    resp = client.put(
        f"/comments/{cid}",
        params={"user_id": 2},
        json={"content": "Hack"},
    )
    assert resp.status_code == 403, resp.text


def test_comment_delete_forbidden_other_user(client):
    # Create with user 1
    created = client.post(
        "/comments",
        params={"user_id": 1},
        json={"content": "Propio", "startup_id": 1},
    )
    assert created.status_code == 201
    cid = created.json()["comment_id"]

    # Try to delete with user 2
    resp = client.delete(f"/comments/{cid}", params={"user_id": 2})
    assert resp.status_code == 403


def test_vote_upsert_user_not_found(client):
    resp = client.post(
        "/votes",
        params={"user_id": 999},
        json={"startup_id": 1, "vote_type": "upvote"},
    )
    assert resp.status_code == 404


def test_vote_upsert_startup_not_found(client):
    resp = client.post(
        "/votes",
        params={"user_id": 1},
        json={"startup_id": 999, "vote_type": "upvote"},
    )
    assert resp.status_code == 404


def test_vote_delete_not_found(client):
    # No vote exists yet for user 1 on startup 1
    resp = client.delete("/votes", params={"user_id": 1, "startup_id": 1})
    assert resp.status_code == 404


def test_comment_create_empty_content_422(client):
    resp = client.post(
        "/comments",
        params={"user_id": 1},
        json={"content": "", "startup_id": 1},
    )
    assert resp.status_code == 422


def test_vote_invalid_type_422(client):
    resp = client.post(
        "/votes",
        params={"user_id": 1},
        json={"startup_id": 1, "vote_type": "invalid"},
    )
    assert resp.status_code == 422
