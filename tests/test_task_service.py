import pytest

from src.task_service import TaskInput, validate_task


def test_rejeita_titulo_vazio():
    with pytest.raises(ValueError, match="título"):
        validate_task(TaskInput(title="", priority="alta"))


def test_rejeita_prioridade_invalida():
    with pytest.raises(ValueError, match="Prioridade"):
        validate_task(TaskInput(title="Separar pedido", priority="urgente"))


def test_cria_tarefa_com_status_inicial():
    task = validate_task(TaskInput(title="Separar pedido", priority="critica"))
    assert task.status == "A_FAZER"
    assert task.priority == "critica"
