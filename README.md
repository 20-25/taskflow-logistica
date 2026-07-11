# TaskFlow Logística

Sistema web acadêmico para gerenciamento de tarefas de uma startup de logística. O projeto
aplica Engenharia de Software, metodologia ágil híbrida Scrum-Kanban, versionamento no
GitHub, testes automatizados e integração contínua.

## Objetivo

Centralizar tarefas operacionais e permitir cadastro, consulta, edição, exclusão, atribuição de
responsável, atualização de status e acompanhamento por prioridade.

## Funcionalidades

- login de demonstração;
- CRUD completo de tarefas;
- status **A Fazer**, **Em Progresso** e **Concluído**;
- responsável e prazo;
- painel com contagem por status;
- classificação de prioridade;
- filtro para tarefas críticas;
- testes automatizados com Pytest;
- análise de qualidade com Flake8;
- integração contínua com GitHub Actions.

## Mudança de escopo

O escopo inicial previa o gerenciamento por status. Após a revisão do primeiro incremento,
foi incluído o campo de prioridade com as opções baixa, média, alta e crítica, além de um filtro
para exibir somente tarefas críticas. A alteração permite destacar ocorrências urgentes da
operação logística e foi refletida no código, nos testes, na modelagem e no Kanban.

## Estrutura do repositório

```text
.github/workflows/ci.yml  # pipeline de testes e qualidade
docs/                     # UML, Kanban, commits e evidências
src/                      # aplicação Flask
tests/                    # testes Pytest
requirements.txt          # dependências
run.py                    # inicialização da aplicação
```

## Como executar no Windows

1. Instale o Python 3.12 ou versão compatível.
2. Abra o terminal na pasta do projeto.
3. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

4. Instale as dependências:

```powershell
pip install -r requirements.txt
```

5. Inicialize o banco e, opcionalmente, os dados de demonstração:

```powershell
flask --app run.py init-db
flask --app run.py seed-db
```

6. Inicie o sistema:

```powershell
flask --app run.py run --debug
```

7. Acesse `http://127.0.0.1:5000` no navegador.

### Login de demonstração

- Usuário: `admin`
- Senha: `admin123`

Esses dados são apenas para apresentação acadêmica. Em produção, as credenciais devem ser
armazenadas com segurança e definidas por variáveis de ambiente.

## Como executar os testes

```powershell
python -m pytest -q
python -m flake8 src tests run.py
```

## Metodologia ágil

O projeto utiliza um modelo híbrido Scrum-Kanban. O desenvolvimento ocorre em pequenos
incrementos, enquanto o GitHub Projects mostra o fluxo dos cards nas colunas To Do, In
Progress e Done. A definição de pronto exige código implementado, testado, documentado e
aprovado no GitHub Actions.

## Documentação complementar

- [Modelagem UML](docs/uml.md)
- [Cards do Kanban](docs/kanban.md)
- [Roteiro de commits](docs/roteiro_commits.md)
- [Checklist de evidências](docs/evidencias.md)
