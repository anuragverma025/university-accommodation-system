import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_session

client = TestClient(app)

def test_report_hall_managers_unauthorized():
    """Test that reports require authentication."""
    response = client.get("/api/reports/hall-managers")
    assert response.status_code == 401

def test_get_entity_students():
    """Test fetching students entity with admin token."""
    # First login as admin
    login_res = client.post("/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = login_res.json()["access_token"]
    
    response = client.get("/api/students", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_non_existent_entity():
    """Test that requesting a non-existent entity returns 404."""
    login_res = client.post("/auth/login", json={"username": "admin", "password": "Admin@123"})
    token = login_res.json()["access_token"]
    
    response = client.get("/api/ghost_entity", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404

def test_health_check():
    """Simple health check test."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
