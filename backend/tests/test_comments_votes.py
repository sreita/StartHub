import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import (
    create_engine,
    text,
    Table,
    Column,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from backend.main import app
from backend.db.base import Base
from backend.db.session import get_db


@pytest.fixture(scope="session")
def test_engine():
    # SQLite en memoria para pruebas
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Registrar tablas mínimas para FK y validaciones (User, Category, Startup)
    # en el mismo Base.metadata antes de create_all para evitar errores de FK.
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

    # Crear todas las tablas (incluye Comment, Vote y las stubs anteriores)
    Base.metadata.create_all(bind=engine)

    # Seed mínimo: user=1, category=1, startup=1
    with engine.begin() as conn:
        conn.exec_driver_sql("INSERT INTO Category (name) VALUES ('General');")
        conn.exec_driver_sql(
            "INSERT INTO `User` (email, password_hash, first_name, last_name, is_enabled) VALUES (" \
            "'tester@example.com','hash','Tester','One',1);"
        )
        conn.exec_driver_sql(
            "INSERT INTO Startup (name, description, owner_user_id, category_id) VALUES (" \
            "'Demo','Desc',1,1);"
        )
    return engine


@pytest.fixture()
def db_session(test_engine) -> Generator:
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def override_dependency(db_session):
    # Override del get_db de la app para usar la sesión de test
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


def test_comments_crud(client):
    # Crear comentario
    resp = client.post(
        "/comments",
        params={"user_id": 1},
        json={"content": "Comentario inicial", "startup_id": 1},
    )
    assert resp.status_code == 201, resp.text
    created = resp.json()
    assert created["content"] == "Comentario inicial"
    assert created["startup_id"] == 1
    comment_id = created["comment_id"]

    # Listar por startup
    resp = client.get("/comments", params={"startup_id": 1})
    assert resp.status_code == 200
    items = resp.json()
    assert any(c["comment_id"] == comment_id for c in items)

    # Editar
    resp = client.put(
        f"/comments/{comment_id}",
        params={"user_id": 1},
        json={"content": "Comentario editado"},
    )
    assert resp.status_code == 200, resp.text
    updated = resp.json()
    assert updated["content"] == "Comentario editado"

    # Eliminar
    resp = client.delete(f"/comments/{comment_id}", params={"user_id": 1})
    assert resp.status_code == 204, resp.text

    # Verificar eliminado
    resp = client.get("/comments", params={"startup_id": 1})
    assert resp.status_code == 200
    items = resp.json()
    assert all(c["comment_id"] != comment_id for c in items)


def test_votes_flow(client):
    # Crear upvote → 201
    resp = client.post(
        "/votes",
        params={"user_id": 1},
        json={"startup_id": 1, "vote_type": "upvote"},
    )
    assert resp.status_code == 201, resp.text
    v1 = resp.json()
    assert v1["vote_type"] == "upvote"

    # Cambiar a downvote → 200
    resp = client.post(
        "/votes",
        params={"user_id": 1},
        json={"startup_id": 1, "vote_type": "downvote"},
    )
    assert resp.status_code == 200, resp.text
    v2 = resp.json()
    assert v2["vote_type"] == "downvote"

    # Conteo
    resp = client.get("/votes/count/1")
    assert resp.status_code == 200, resp.text
    counts = resp.json()
    assert counts["startup_id"] == 1
    assert counts["downvotes"] >= 1

    # Eliminar voto
    resp = client.delete("/votes", params={"user_id": 1, "startup_id": 1})
    assert resp.status_code == 204, resp.text

    # Conteo después de eliminar
    resp = client.get("/votes/count/1")
    assert resp.status_code == 200
    counts_after = resp.json()
    # downvotes deberían ser >= 0; al menos no mayor que antes
    assert counts_after["downvotes"] <= counts["downvotes"]
