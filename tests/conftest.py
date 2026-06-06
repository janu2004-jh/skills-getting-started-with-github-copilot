from copy import deepcopy

from fastapi.testclient import TestClient
import pytest

from src import app as app_module

_original_activities = deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = deepcopy(_original_activities)
    yield
    app_module.activities = deepcopy(_original_activities)

@pytest.fixture
def client():
    return TestClient(app_module.app)
