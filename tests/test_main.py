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


def test_calculate_sum():
    # Validates the newly added /calculate/sum endpoint for the basic
    # positive-number case
    response = client.get("/calculate/sum?a=7&b=5")

    assert response.status_code == 200
    data = response.json()

    # Check field values
    assert data == {"a": 7, "b": 5, "result": 12}


def test_calculate_sum_negative():
    # Covers the negative-number scenario for the new sum endpoint
    response = client.get("/calculate/sum?a=-3&b=8")

    assert response.status_code == 200
    data = response.json()

    # Check field values
    assert data["a"] == -3
    assert data["b"] == 8


def test_calculate_multiply():
    # Validates the newly added /calculate/multiply endpoint for the basic
    # positive-number case
    response = client.get("/calculate/multiply?a=7&b=5")

    assert response.status_code == 200
    data = response.json()

    # Check field values
    assert data == {"a": 7, "b": 5, "result": 35}


def test_calculate_multiply_negative():
    # Covers the negative-number scenario for the new multiply endpoint
    response = client.get("/calculate/multiply?a=-3&b=8")

    assert response.status_code == 200
    data = response.json()

    # Check field values
    assert data["a"] == -3
    assert data["b"] == 8
    assert data["result"] == -24


def test_calculate_sum_missing_param():
    # Verifies FastAPI's automatic 422 response when a required query
    # parameter is omitted (here, 'b' is missing)
    response = client.get("/calculate/sum?a=7")

    assert response.status_code == 422


def test_calculate_multiply_missing_param():
    # Covers the missing required query parameter scenario for the new
    # multiply endpoint; FastAPI's built-in validation should return 422
    response = client.get("/calculate/multiply?a=7")

    assert response.status_code == 422


def test_calculate_divide():
    # Validates the newly added /calculate/divide endpoint for the basic
    # positive-number case
    response = client.get("/calculate/divide?a=10&b=2")

    assert response.status_code == 200
    data = response.json()

    # Check field values
    assert data == {"a": 10, "b": 2, "result": 5, "operation": "divide"}


def test_calculate_divide_negative():
    # Covers the negative-number scenario for the new divide endpoint
    response = client.get("/calculate/divide?a=-9&b=3")

    assert response.status_code == 200
    data = response.json()

    # Check field values
    assert data["a"] == -9
    assert data["b"] == 3
    assert data["result"] == -3
    assert data["operation"] == "divide"


def test_calculate_divide_by_zero():
    # Verifies that dividing by zero returns HTTP 400 as required
    response = client.get("/calculate/divide?a=10&b=0")

    assert response.status_code == 400
    assert response.json() == {"detail": "Division by zero is not allowed"}


def test_calculate_divide_missing_param():
    # Covers the missing required query parameter scenario for the new
    # divide endpoint; FastAPI's built-in validation should return 422
    response = client.get("/calculate/divide?a=10")

    assert response.status_code == 422
