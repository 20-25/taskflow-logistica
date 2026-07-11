from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from src import create_app
from src.db import get_db, init_db


@pytest.fixture()
def app():
    with tempfile.TemporaryDirectory() as temp_dir:
        database = Path(temp_dir) / "test.sqlite"
        app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-key",
                "DATABASE": str(database),
                "DEMO_USERNAME": "admin",
                "DEMO_PASSWORD": "admin123",
            }
        )
        with app.app_context():
            init_db()
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def authenticated_client(client):
    client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )
    return client


@pytest.fixture()
def task_id(app):
    with app.app_context():
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO tasks
                (title, description, responsible, deadline, status, priority)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "Separar pedido",
                "Pedido para entrega imediata",
                "Ana",
                "2026-07-15",
                "A_FAZER",
                "critica",
            ),
        )
        db.commit()
        return cursor.lastrowid
