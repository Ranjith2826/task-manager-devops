
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = __import__(
    "sqlalchemy.orm", fromlist=["sessionmaker"]
).sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_create_and_list_task():
    with TestClient(app) as client:
        response = client.post(
            "/api/tasks",
            json={"title": "Learn Docker"}
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Learn Docker"

        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert any(
            task["title"] == "Learn Docker"
            for task in response.json()
        )

def test_reject_empty_title():
    with TestClient(app) as client:
        response = client.post("/api/tasks", json={"title": ""})
        assert response.status_code == 422
