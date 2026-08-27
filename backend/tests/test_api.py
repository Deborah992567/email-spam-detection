"""
Unit tests for the backend API.
"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


# Mock database before importing app
@pytest.fixture(autouse=True)
def mock_db():
    with patch("backend.app.database.connection.engine"):
        with patch("backend.app.database.connection.SessionLocal"):
            yield


@pytest.fixture
def client():
    from backend.app.main import app
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_register_validation(client):
    response = client.post("/api/auth/register", json={
        "name": "A",
        "email": "invalid-email",
        "password": "123",
    })
    assert response.status_code == 422


def test_login_validation(client):
    response = client.post("/api/auth/login", json={
        "email": "not-an-email",
        "password": "",
    })
    assert response.status_code == 422
