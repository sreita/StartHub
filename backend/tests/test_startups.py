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
    # SQLite en memoria para pruebas
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Registrar tablas mínimas para FK y validaciones
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

    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    # Seed mínimo: user=1, category=1, startup=1
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
            "'Demo Startup','Demo Description',1,1);"
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


def test_create_startup_success(client):
    """Test crear startup exitosamente"""
    resp = client.post(
        "/startups",
        params={"user_id": 1},
        json={
            "name": "Nueva Startup Test",
            "description": "Descripción de prueba",
            "category_id": 1
        },
    )
    assert resp.status_code == 201, resp.text
    created = resp.json()
    assert created["name"] == "Nueva Startup Test"
    assert created["description"] == "Descripción de prueba"
    assert created["owner_user_id"] == 1
    assert created["category_id"] == 1
    assert "startup_id" in created


def test_create_startup_invalid_data(client):
    """Test crear startup con datos inválidos"""
    # Nombre vacío
    resp = client.post(
        "/startups",
        params={"user_id": 1},
        json={
            "name": "",
            "description": "Descripción",
            "category_id": 1
        },
    )
    assert resp.status_code == 400, resp.text


def test_get_startup_success(client):
    """Test obtener startup por ID"""
    resp = client.get("/startups/1")
    assert resp.status_code == 200, resp.text
    startup = resp.json()
    assert startup["startup_id"] == 1
    assert startup["name"] == "Demo Startup"


def test_get_startup_not_found(client):
    """Test obtener startup que no existe"""
    resp = client.get("/startups/999")
    assert resp.status_code == 404, resp.text


def test_list_startups(client):
    """Test listar todas las startups"""
    resp = client.get("/startups")
    assert resp.status_code == 200, resp.text
    startups = resp.json()
    assert isinstance(startups, list)
    assert len(startups) >= 1


def test_list_my_startups(client):
    """Test listar startups de un usuario específico"""
    resp = client.get("/startups/my-startups", params={"user_id": 1})
    assert resp.status_code == 200, resp.text
    my_startups = resp.json()
    assert isinstance(my_startups, list)
    # Debe incluir la startup demo que tiene owner_user_id=1
    assert any(s["owner_user_id"] == 1 for s in my_startups)


def test_update_startup_success(client):
    """Test actualizar startup exitosamente"""
    # Primero crear una startup
    create_resp = client.post(
        "/startups",
        params={"user_id": 1},
        json={
            "name": "Startup a actualizar",
            "description": "Descripción original",
            "category_id": 1
        },
    )
    assert create_resp.status_code == 201, create_resp.text
    startup_id = create_resp.json()["startup_id"]

    # Actualizar
    resp = client.put(
        f"/startups/{startup_id}",
        params={"user_id": 1},
        json={
            "name": "Startup actualizada",
            "description": "Nueva descripción"
        },
    )
    assert resp.status_code == 200, resp.text
    updated = resp.json()
    assert updated["name"] == "Startup actualizada"
    assert updated["description"] == "Nueva descripción"


def test_update_startup_unauthorized(client):
    """Test actualizar startup de otro usuario (debe fallar)"""
    # La startup demo es del usuario 1
    resp = client.put(
        "/startups/1",
        params={"user_id": 2},  # Usuario 2 intenta editar startup del usuario 1
        json={
            "name": "Nombre hackeado",
        },
    )
    assert resp.status_code == 403, resp.text


def test_delete_startup_success(client):
    """Test eliminar startup exitosamente"""
    # Primero crear una startup para eliminar
    create_resp = client.post(
        "/startups",
        params={"user_id": 1},
        json={
            "name": "Startup a eliminar",
            "description": "Descripción",
            "category_id": 1
        },
    )
    assert create_resp.status_code == 201, create_resp.text
    startup_id = create_resp.json()["startup_id"]

    # Eliminar
    resp = client.delete(f"/startups/{startup_id}", params={"user_id": 1})
    assert resp.status_code == 204, resp.text

    # Verificar que ya no existe
    get_resp = client.get(f"/startups/{startup_id}")
    assert get_resp.status_code == 404, get_resp.text


def test_delete_startup_unauthorized(client):
    """Test eliminar startup de otro usuario (debe fallar)"""
    # La startup demo es del usuario 1
    resp = client.delete("/startups/1", params={"user_id": 2})
    assert resp.status_code == 403, resp.text


def test_get_startup_with_stats(client):
    """Test obtener startup con estadísticas"""
    resp = client.get("/startups/1/with-stats")
    assert resp.status_code == 200, resp.text
    startup = resp.json()
    assert startup["startup_id"] == 1
    assert "total_votos" in startup
    assert "total_comentarios" in startup