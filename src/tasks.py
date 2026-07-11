from __future__ import annotations

import sqlite3

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from . import login_required
from .db import get_db
from .task_service import (
    ALLOWED_PRIORITIES,
    ALLOWED_STATUSES,
    TaskInput,
    validate_task,
)

bp = Blueprint("tasks", __name__)


def get_task_or_404(task_id: int) -> sqlite3.Row:
    task = get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        abort(404)
    return task


@bp.route("/")
@login_required
def index():
    db = get_db()
    priority = request.args.get("priority", "").strip().lower()
    status = request.args.get("status", "").strip().upper()

    query = "SELECT * FROM tasks WHERE 1 = 1"
    parameters: list[str] = []

    if priority in ALLOWED_PRIORITIES:
        query += " AND priority = ?"
        parameters.append(priority)
    if status in ALLOWED_STATUSES:
        query += " AND status = ?"
        parameters.append(status)

    query += " ORDER BY CASE priority WHEN 'critica' THEN 1 WHEN 'alta' THEN 2 "
    query += "WHEN 'media' THEN 3 ELSE 4 END, deadline, id DESC"
    tasks = db.execute(query, parameters).fetchall()

    counts = {
        row["status"]: row["total"]
        for row in db.execute(
            "SELECT status, COUNT(*) AS total FROM tasks GROUP BY status"
        ).fetchall()
    }

    return render_template(
        "index.html",
        tasks=tasks,
        counts=counts,
        statuses=ALLOWED_STATUSES,
        priorities=ALLOWED_PRIORITIES,
        selected_status=status,
        selected_priority=priority,
    )


def form_task_input() -> TaskInput:
    return TaskInput(
        title=request.form.get("title", ""),
        description=request.form.get("description", ""),
        responsible=request.form.get("responsible", ""),
        deadline=request.form.get("deadline", ""),
        status=request.form.get("status", "A_FAZER"),
        priority=request.form.get("priority", "media"),
    )


@bp.route("/tasks/new", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        try:
            task = validate_task(form_task_input())
        except ValueError as error:
            flash(str(error), "danger")
        else:
            db = get_db()
            db.execute(
                """
                INSERT INTO tasks
                    (title, description, responsible, deadline, status, priority)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    task.title,
                    task.description,
                    task.responsible,
                    task.deadline,
                    task.status,
                    task.priority,
                ),
            )
            db.commit()
            flash("Tarefa cadastrada com sucesso.", "success")
            return redirect(url_for("tasks.index"))

    return render_template(
        "task_form.html",
        task=None,
        statuses=ALLOWED_STATUSES,
        priorities=ALLOWED_PRIORITIES,
    )


@bp.route("/tasks/<int:task_id>/edit", methods=("GET", "POST"))
@login_required
def edit(task_id: int):
    existing_task = get_task_or_404(task_id)

    if request.method == "POST":
        try:
            task = validate_task(form_task_input())
        except ValueError as error:
            flash(str(error), "danger")
        else:
            db = get_db()
            db.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, responsible = ?, deadline = ?,
                    status = ?, priority = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    task.title,
                    task.description,
                    task.responsible,
                    task.deadline,
                    task.status,
                    task.priority,
                    task_id,
                ),
            )
            db.commit()
            flash("Tarefa atualizada com sucesso.", "success")
            return redirect(url_for("tasks.index"))

    return render_template(
        "task_form.html",
        task=existing_task,
        statuses=ALLOWED_STATUSES,
        priorities=ALLOWED_PRIORITIES,
    )


@bp.post("/tasks/<int:task_id>/status")
@login_required
def update_status(task_id: int):
    get_task_or_404(task_id)
    status = request.form.get("status", "").strip().upper()
    if status not in ALLOWED_STATUSES:
        flash("Status inválido.", "danger")
        return redirect(url_for("tasks.index"))

    db = get_db()
    db.execute(
        "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (status, task_id),
    )
    db.commit()
    flash("Status atualizado.", "success")
    return redirect(url_for("tasks.index"))


@bp.post("/tasks/<int:task_id>/delete")
@login_required
def delete(task_id: int):
    get_task_or_404(task_id)
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    flash("Tarefa excluída.", "success")
    return redirect(url_for("tasks.index"))
