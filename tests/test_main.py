import re
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    
    # Check that all required fields are present
    assert "status" in data
    assert "version" in data
    assert "timestamp" in data
    
    # Check field values
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"
    
    # Validate timestamp is in ISO 8601 format (UTC)
    iso_8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?\+00:00$'
    assert re.match(iso_8601_pattern, data["timestamp"]), f"Timestamp {data['timestamp']} is not in valid ISO 8601 UTC format"


def test_info():
    response = client.get("/info")

    assert response.status_code == 200
    data = response.json()
    
    # Check that all required fields are present
    assert "service_name" in data
    assert "application_version" in data
    assert "environment" in data
    
    # Check field values
    assert data["service_name"] == "issue-to-pr-test-repo"
    assert data["application_version"] == "1.0.0"
    assert data["environment"] == "development"


def test_ready():
    response = client.get("/ready")

    assert response.status_code == 200
    data = response.json()

    # Check that all required fields are present
    assert "status" in data
    assert "service" in data
    assert "version" in data

    # Check field values
    assert data["status"] == "ready"
    assert data["service"] == "issue-to-pr-test-repo"
    assert data["version"] == app.version


def test_ping():
    response = client.get("/ping")

    assert response.status_code == 200
    data = response.json()

    # Check that all required fields are present
    assert "status" in data
    assert "service" in data

    # Check field values
    assert data["status"] == "ping"
    assert data["service"] == "issue-to-pr-test-repo"
