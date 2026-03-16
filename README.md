# FastAPI Task Manager SaaS API

API de gerenciamento de tarefas desenvolvida com **FastAPI**, utilizando **PostgreSQL** como banco de dados, **Redis** para cache e filas assíncronas com **Celery**.

Projeto criado para estudo de **arquitetura backend moderna**, incluindo autenticação, filas assíncronas, rate limiting, migrations de banco e deploy com Docker.

---

## Tecnologias

- **FastAPI** – Framework principal da API
- **PostgreSQL** – Banco de dados relacional
- **SQLAlchemy** – ORM para acesso ao banco
- **Alembic** – Versionamento de migrations do banco
- **Redis** – Cache e broker de filas
- **Celery** – Processamento de tarefas assíncronas
- **SlowAPI** – Rate limiting por IP
- **Pydantic** – Validação de dados
- **Python-dotenv** – Gerenciamento de variáveis de ambiente
- **Uvicorn** – Servidor ASGI
- **Docker / Docker Compose** – Containerização

---

## Funcionalidades

- Registro e autenticação de usuários
- CRUD completo de **Projetos**
- CRUD completo de **Tarefas**
- Filtragem de tarefas por status ou projeto
- Paginação de resultados
- Rate limiting em endpoints sensíveis
- Execução de tarefas assíncronas com Celery
- Logs estruturados da aplicação
- Migrations de banco com Alembic
- Deploy completo com Docker Compose

---

## Arquitetura

Client  
│  
▼ Routers (FastAPI)  
│  
▼ Service Layer (Regras de negócio)  
│  
▼ Repositories (Acesso aos dados)  
│  
▼ Models (SQLAlchemy ORM)  
│  
▼ PostgreSQL + Redis

Workers (Celery)  
│  
▼ Tarefas assíncronas

---

## Estrutura do projeto

```
app/
├── api/
│   └── routes/
│
├── core/
│   ├── security.py
│   ├── limiter.py
│   └── log_middleware.py
│
├── db/
│   └── database.py
│
├── models/
│   ├── user.py
│   ├── project.py
│   └── task.py
│
├── repositories/
│
├── schemas/
│
├── services/
│
├── workers/
│   └── tasks.py
│
└── main.py
```

---

## Objetivo

Este projeto foi desenvolvido para prática de **desenvolvimento backend profissional com FastAPI**, aplicando conceitos de arquitetura em camadas, processamento assíncrono, controle de requisições, migrations de banco e containerização com Docker.

---

## Rodando o projeto

Clone o repositório:

```bash
git clone https://github.com/HighOffGrid/task-manager-saas-api
cd task-manager-saas-api
```

---

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Rodando com Docker

O projeto já vem configurado com **Docker e Docker Compose**, incluindo PostgreSQL e Redis.

Execute:

```bash
docker compose up --build
```

Isso irá iniciar:

- API FastAPI
- PostgreSQL
- Redis
- Worker Celery

---

## Executando a API

Para rodar apenas a API em desenvolvimento:

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## Filas Assíncronas

As tarefas assíncronas são processadas usando **Celery + Redis**.

Para iniciar o worker manualmente:

```bash
celery -A app.workers.celery_app worker --loglevel=info
```

---

## Rate Limiting

Endpoints críticos possuem limitação de requisições usando **SlowAPI + Redis**.

Exemplo:

```
5 requisições por minuto por IP
```

---

## Autor

Projeto desenvolvido para estudo de **arquitetura backend moderna e práticas utilizadas em empresas de tecnologia.**
