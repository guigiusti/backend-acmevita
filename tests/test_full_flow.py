import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.configs import Config
import os

os.environ["ENV"] = "development"

BASE_URL =f"http://{Config.APP.HOST}:{Config.APP.PORT}{Config.APP.ROOT_PATH}"

@pytest.fixture
def client():
    return TestClient(app, base_url=BASE_URL)

def test_full_flow(client):
    response = client.delete("/clear-db")
    assert response.status_code == 204

    response = client.post("/department", json={"name": "Department 1"})
    assert response.status_code == 201, response.text
    assert response.json() == {"id": 1, "name": "Department 1"}

    response = client.post("/employee", json={"name": "Employee 1", "department_id": "1"})
    assert response.status_code == 201, response.text
    assert response.json() == {"id": 1, "name": "Employee 1", "department_id": 1, "have_dependents": False, "dependents": []}

    response = client.post("/employee", json={"name": "Employee 2", "department_id": "1", "dependents": [{"name": "Dependent 1"}]})
    assert response.status_code == 201, response.text
    assert response.json() == {"id": 2, "name": "Employee 2", "department_id": 1, "have_dependents": True, "dependents": [{"name": "Dependent 1"}]}

    response = client.get("/employee/1")
    assert response.status_code == 200
    assert response.json() == [{"name": "Employee 1", "have_dependents": False}, {"name": "Employee 2", "have_dependents": True}]

    response = client.get("/department")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Department 1"}]

    response = client.delete("/clear-db")
    assert response.status_code == 204