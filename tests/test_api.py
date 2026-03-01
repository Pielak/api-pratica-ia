import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"  # banco em memória

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_criar_tarefa():
    response = client.post(
        "/tarefas", json={"titulo": "Estudar FastAPI", "descricao": "Ver docs oficiais"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Estudar FastAPI"
    assert data["concluida"] is False
    assert "id" in data


def test_listar_tarefas():
    client.post("/tarefas", json={"titulo": "T1", "descricao": "D1"})
    client.post("/tarefas", json={"titulo": "T2", "descricao": "D2"})
    response = client.get("/tarefas")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_listar_paginacao():
    for i in range(5):
        client.post("/tarefas", json={"titulo": f"T{i}", "descricao": f"D{i}"})
    response = client.get("/tarefas?skip=0&limit=3")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_buscar_tarefa():
    res = client.post("/tarefas", json={"titulo": "T1", "descricao": "D1"})
    id = res.json()["id"]
    response = client.get(f"/tarefas/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == id


def test_buscar_tarefa_nao_encontrada():
    response = client.get("/tarefas/9999")
    assert response.status_code == 404


def test_atualizar_tarefa():
    res = client.post("/tarefas", json={"titulo": "T1", "descricao": "D1"})
    id = res.json()["id"]
    response = client.put(f"/tarefas/{id}", json={"concluida": True})
    assert response.status_code == 200
    assert response.json()["concluida"] is True
    assert response.json()["titulo"] == "T1"


def test_atualizar_tarefa_nao_encontrada():
    response = client.put("/tarefas/9999", json={"concluida": True})
    assert response.status_code == 404


def test_deletar_tarefa():
    res = client.post("/tarefas", json={"titulo": "T1", "descricao": "D1"})
    id = res.json()["id"]
    response = client.delete(f"/tarefas/{id}")
    assert response.status_code == 204
    assert client.get(f"/tarefas/{id}").status_code == 404


def test_deletar_tarefa_nao_encontrada():
    response = client.delete("/tarefas/9999")
    assert response.status_code == 404
