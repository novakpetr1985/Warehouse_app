from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def create_material(client: TestClient, quantity: int = 10) -> int:
    response = client.post(
        "/materials/",
        json={
            "name": "Test material",
            "quantity": quantity,
            "qr_code": "TEST-001",
            "location": "TEST",
        },
    )
    assert response.status_code == 200
    return response.json()["id"]


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_material(client: TestClient):
    material_id = create_material(client)

    response = client.get(f"/materials/{material_id}")
    assert response.status_code == 200
    assert response.json()["quantity"] == 10


def test_missing_material_returns_404(client: TestClient):
    response = client.get("/materials/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Material not found"


def test_delete_material(client: TestClient):
    material_id = create_material(client)

    response = client.delete(f"/materials/{material_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}

    assert client.get(f"/materials/{material_id}").status_code == 404


def test_in_movement_increases_stock(client: TestClient):
    material_id = create_material(client, quantity=10)

    response = client.post(
        "/movements/",
        json={"material_id": material_id, "movement_type": "IN", "quantity": 5},
    )
    assert response.status_code == 200
    assert response.json()["material"]["quantity"] == 15
    assert response.json()["movement"]["id"]


def test_out_movement_decreases_stock(client: TestClient):
    material_id = create_material(client, quantity=10)

    response = client.post(
        "/movements/",
        json={"material_id": material_id, "movement_type": "OUT", "quantity": 4},
    )
    assert response.status_code == 200
    assert response.json()["material"]["quantity"] == 6


def test_out_movement_rejects_insufficient_stock(client: TestClient):
    material_id = create_material(client, quantity=3)

    response = client.post(
        "/movements/",
        json={"material_id": material_id, "movement_type": "OUT", "quantity": 4},
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Not enough stock"


def test_movement_validation_rejects_invalid_input(client: TestClient):
    material_id = create_material(client)

    response = client.post(
        "/movements/",
        json={"material_id": material_id, "movement_type": "TRANSFER", "quantity": 0},
    )
    assert response.status_code == 422
