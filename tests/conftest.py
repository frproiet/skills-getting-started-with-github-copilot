import copy

import pytest
from fastapi.testclient import TestClient

from src import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app.app)

@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app.activities)
    yield
    app.activities = original
