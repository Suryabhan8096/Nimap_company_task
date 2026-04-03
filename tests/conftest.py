import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.database.session import get_db
from main import app

TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    })
    return response.json()


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client):
    # Register admin user
    client.post("/auth/register", json={
        "email": "admin@example.com",
        "username": "adminuser",
        "password": "adminpass123",
    })
    # Manually set role to admin in DB
    db = TestSession()
    from app.models.user import User
    from app.enums import UserRole
    user = db.query(User).filter(User.username == "adminuser").first()
    user.role = UserRole.ADMIN
    db.commit()
    db.close()

    response = client.post("/auth/login", json={
        "username": "adminuser",
        "password": "adminpass123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def analyst_headers(client):
    client.post("/auth/register", json={
        "email": "analyst@example.com",
        "username": "analystuser",
        "password": "analystpass123",
    })
    db = TestSession()
    from app.models.user import User
    from app.enums import UserRole
    user = db.query(User).filter(User.username == "analystuser").first()
    user.role = UserRole.ANALYST
    db.commit()
    db.close()

    response = client.post("/auth/login", json={
        "username": "analystuser",
        "password": "analystpass123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
