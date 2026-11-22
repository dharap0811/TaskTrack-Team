
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class FakeRedis:
    def __init__(self):
        self.tasks = {}

    def ping(self):
        return True

    def hset(self, name, key, value):
        self.tasks[key] = value

    def hvals(self, name):
        return list(self.tasks.values())

    def hget(self, name, key):
        return self.tasks.get(key)


def test_health_endpoint():
    fake_redis = FakeRedis()

    with patch("app.main.get_redis", return_value=fake_redis):
        client = TestClient(app)
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_and_view_tasks():
    fake_redis = FakeRedis()

    with patch("app.main.get_redis", return_value=fake_redis):
        client = TestClient(app)

        created = client.post(
            "/tasks",
            json={"title": "Complete IT 390 project"}
        )

        assert created.status_code == 201
        assert created.json()["completed"] is False

        listed = client.get("/tasks")

        assert listed.status_code == 200
        assert len(listed.json()) == 1
        assert listed.json()[0]["title"] == "Complete IT 390 project"


def test_complete_task():
    fake_redis = FakeRedis()

    with patch("app.main.get_redis", return_value=fake_redis):
        client = TestClient(app)

        created = client.post(
            "/tasks",
            json={"title": "Finish Docker setup"}
        )

        task_id = created.json()["id"]

        completed = client.patch(
            f"/tasks/{task_id}/complete"
        )

        assert completed.status_code == 200
        assert completed.json()["completed"] is True


def test_nonexistent_task():
    fake_redis = FakeRedis()

    with patch("app.main.get_redis", return_value=fake_redis):
        client = TestClient(app)

        response = client.patch(
            "/tasks/nonexistent/complete"
        )

        assert response.status_code == 404


def test_homepage():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "TaskTrack" in response.text
