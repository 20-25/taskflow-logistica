from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import click
from flask import Flask, current_app, g

SCHEMA = """
DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    responsible TEXT NOT NULL DEFAULT '',
    deadline TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'A_FAZER',
    priority TEXT NOT NULL DEFAULT 'media',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_db() -> sqlite3.Connection:
    """Return one SQLite connection per request/application context."""
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_: BaseException | None = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()


def seed_db() -> None:
    """Insert realistic tasks for a quick classroom demonstration."""
    db = get_db()
    sample_tasks: list[tuple[Any, ...]] = [
        (
            "Separar pedidos prioritários",
            "Organizar os pedidos com entrega no mesmo dia.",
            "Ana",
            "2026-07-15",
            "A_FAZER",
            "critica",
        ),
        (
            "Revisar rota de entrega",
            "Conferir possíveis atrasos e atualizar o motorista.",
            "Carlos",
            "2026-07-16",
            "EM_PROGRESSO",
            "alta",
        ),
        (
            "Atualizar relatório de ocorrências",
            "Registrar as ocorrências resolvidas na semana.",
            "Luiza",
            "2026-07-18",
            "CONCLUIDO",
            "media",
        ),
    ]
    db.executemany(
        """
        INSERT INTO tasks
            (title, description, responsible, deadline, status, priority)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        sample_tasks,
    )
    db.commit()


@click.command("init-db")
def init_db_command() -> None:
    init_db()
    click.echo("Banco de dados inicializado.")


@click.command("seed-db")
def seed_db_command() -> None:
    seed_db()
    click.echo("Dados de demonstração adicionados.")


def init_app(app: Flask) -> None:
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
