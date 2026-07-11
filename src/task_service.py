from __future__ import annotations

from dataclasses import dataclass

ALLOWED_STATUSES = {
    "A_FAZER": "A Fazer",
    "EM_PROGRESSO": "Em Progresso",
    "CONCLUIDO": "Concluído",
}

ALLOWED_PRIORITIES = {
    "baixa": "Baixa",
    "media": "Média",
    "alta": "Alta",
    "critica": "Crítica",
}


@dataclass(frozen=True)
class TaskInput:
    title: str
    description: str = ""
    responsible: str = ""
    deadline: str = ""
    status: str = "A_FAZER"
    priority: str = "media"


def validate_task(data: TaskInput) -> TaskInput:
    """Validate and normalize the business rules of a task."""
    title = data.title.strip()
    if not title:
        raise ValueError("O título da tarefa é obrigatório.")

    status = data.status.strip().upper()
    if status not in ALLOWED_STATUSES:
        raise ValueError("Status inválido.")

    priority = data.priority.strip().lower()
    if priority not in ALLOWED_PRIORITIES:
        raise ValueError("Prioridade inválida.")

    return TaskInput(
        title=title,
        description=data.description.strip(),
        responsible=data.responsible.strip(),
        deadline=data.deadline.strip(),
        status=status,
        priority=priority,
    )
