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
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Tablas mínimas
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

    # Seed: dos usuarios, una categoría, una startup
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


def test_create_startup_empty_name(client):
    """Test crear startup con nombre vacío"""
    resp = client.post(
        "/startups",
        params={"user_id": 1},
        json={
            "name": "",
            "description": "Descripción",
            "category_id": 1
        },
    )
    assert resp.status_code == 422, resp.text

def test_update_startup_not_found(client):
    """Test actualizar startup que no existe"""
    resp = client.put(
        "/startups/999",
        params={"user_id": 1},
        json={"name": "No debería funcionar"},
    )
    assert resp.status_code == 404, resp.text


def test_delete_startup_not_found(client):
    """Test eliminar startup que no existe"""
    resp = client.delete("/startups/999", params={"user_id": 1})
    assert resp.status_code == 404, resp.text

def test_get_startup_with_stats_not_found(client):
    """Test obtener estadísticas de startup que no existe"""
    resp = client.get("/startups/999/with-stats")
    assert resp.status_code == 404, resp.text