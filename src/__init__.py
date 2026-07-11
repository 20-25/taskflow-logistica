from __future__ import annotations

import os
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar, cast

from flask import Flask, flash, redirect, request, session, url_for

from .db import close_db, init_app as init_db_commands

F = TypeVar("F", bound=Callable[..., Any])


def login_required(view: F) -> F:
    """Protect a view so only an authenticated demo user can access it."""

    @wraps(view)
    def wrapped_view(*args: Any, **kwargs: Any) -> Any:
        if not session.get("authenticated"):
            flash("Faça login para acessar o sistema.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return cast(F, wrapped_view)


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Application factory used by the web server and the automated tests."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-change-this-key"),
        DATABASE=str(Path(app.instance_path) / "taskflow.sqlite"),
        DEMO_USERNAME=os.environ.get("TASKFLOW_USERNAME", "admin"),
        DEMO_PASSWORD=os.environ.get("TASKFLOW_PASSWORD", "admin123"),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from . import auth, tasks

    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.teardown_appcontext(close_db)
    init_db_commands(app)

    return app
