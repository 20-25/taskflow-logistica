from src.db import get_db


def test_redireciona_usuario_nao_autenticado(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_com_credenciais_validas(client):
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Painel de tarefas" in response.get_data(as_text=True)


def test_cadastra_tarefa(authenticated_client, app):
    response = authenticated_client.post(
        "/tasks/new",
        data={
            "title": "Revisar rota",
            "description": "Analisar atraso",
            "responsible": "Carlos",
            "deadline": "2026-07-20",
            "status": "A_FAZER",
            "priority": "alta",
        },
        follow_redirects=True,
    )
    assert "Tarefa cadastrada com sucesso" in response.get_data(as_text=True)

    with app.app_context():
        task = get_db().execute(
            "SELECT * FROM tasks WHERE title = ?", ("Revisar rota",)
        ).fetchone()
        assert task is not None
        assert task["priority"] == "alta"


def test_filtra_tarefas_criticas(authenticated_client, task_id):
    response = authenticated_client.get("/?priority=critica")
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Separar pedido" in page
    assert "Crítica" in page


def test_atualiza_status(authenticated_client, app, task_id):
    response = authenticated_client.post(
        f"/tasks/{task_id}/status",
        data={"status": "EM_PROGRESSO"},
        follow_redirects=True,
    )
    assert "Status atualizado" in response.get_data(as_text=True)

    with app.app_context():
        task = get_db().execute(
            "SELECT status FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        assert task["status"] == "EM_PROGRESSO"


def test_exclui_tarefa(authenticated_client, app, task_id):
    response = authenticated_client.post(
        f"/tasks/{task_id}/delete", follow_redirects=True
    )
    assert "Tarefa excluída" in response.get_data(as_text=True)

    with app.app_context():
        task = get_db().execute(
            "SELECT id FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        assert task is None
