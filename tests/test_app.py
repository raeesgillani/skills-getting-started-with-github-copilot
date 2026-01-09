import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester@mergington.edu for Chess Club" in response.json().get("message", "")

    # Clean up: remove the test participant
    data = client.get("/activities").json()
    data["Chess Club"]["participants"].remove("tester@mergington.edu")

def test_signup_duplicate():
    # Add a participant first
    client.post("/activities/Chess Club/signup?email=dupe@mergington.edu")
    # Try to add again
    response = client.post("/activities/Chess Club/signup?email=dupe@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    data = client.get("/activities").json()
    data["Chess Club"]["participants"].remove("dupe@mergington.edu")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
