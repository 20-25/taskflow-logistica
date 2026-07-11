from __future__ import annotations

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        valid_user = username == current_app.config["DEMO_USERNAME"]
        valid_password = password == current_app.config["DEMO_PASSWORD"]
        if valid_user and valid_password:
            session.clear()
            session["authenticated"] = True
            session["username"] = username
            flash("Login realizado com sucesso.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("tasks.index"))

        flash("Usuário ou senha inválidos.", "danger")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "success")
    return redirect(url_for("auth.login"))
