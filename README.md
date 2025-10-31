# 📘 App Observability — Documentação da API

> API desenvolvida em **FastAPI** com **SQLAlchemy**, **OpenTelemetry**, e instrumentação para rastreamento e logs.

---

## ✅ Visão Geral

Esta aplicação expõe uma API para gerenciamento de pessoas, com foco em monitoramento e observabilidade.

📦 Inclui:

* CRUD completo de Pessoa
* SQLite como banco de dados
* OpenTelemetry (tracing + logs)
* Rota de teste com spans manuais
* Estrutura modular e escalável

---

## 🏗 Estrutura do Projeto

```
app/
 ├── app.py               # App FastAPI + OTEL
 ├── crud.py              # Lógica de acesso ao BD
 ├── database.py          # Configuração SQLAlchemy
 ├── models.py            # ORM Pessoa
 ├── schemas.py           # Schemas Pydantic
 ├── routes/
 │    └── pessoa_routes.py  # Endpoints CRUD
 └── docs/                # Documentação técnica
.env
README.md
requirements.txt
```

---

## 🚀 Como Rodar o Projeto

### 1️⃣ Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
```

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Iniciar a aplicação

```bash
uvicorn app.app:app --reload
```

📍 Acesse no navegador:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔄 Variáveis de Ambiente (.env)

```ini
OTEL_SERVICE_NAME=app
OTEL_EXPORTER_OTLP_ENDPOINT=host.docker.internal:4317
OTEL_EXPORTER_OTLP_INSECURE=true
OTEL_TRACES_EXPORTER=otlp
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
```

✅ Já incluídas e funcionando

---

## 🧠 Modelos e Schemas

### 🗄 Modelo ORM (Pessoa)

| Campo  | Tipo  | Obrigatório | Observação           |
| ------ | ----- | ----------- | -------------------- |
| id     | int   | Sim         | Primary Key          |
| nome   | str   | Sim         |                      |
| email  | Email | Sim         | Unique               |
| senha  | str   | Sim         | **Recomendado** hash |
| cidade | str   | Não         |                      |
| activo | bool  | Não         | Default=True         |

---

## 🔌 Endpoints Disponíveis

### ✅ Teste de observabilidade

| Método | Endpoint      | Descrição               |
| ------ | ------------- | ----------------------- |
| GET    | `/test-trace` | Gera trace e log manual |

📌 Retorno

```json
{"status": "trace ok"}
```

### ✅ CRUD Pessoa

Base: `/pessoas`

| Método | Endpoint        | Descrição     |
| ------ | --------------- | ------------- |
| POST   | `/pessoas/`     | Criar pessoa  |
| GET    | `/pessoas/`     | Listar todas  |
| GET    | `/pessoas/{id}` | Buscar por ID |
| PUT    | `/pessoas/{id}` | Atualizar     |
| DELETE | `/pessoas/{id}` | Remover       |

Exemplos completos estão em `/docs/endpoints.md` ✅

---

## 🛰 OpenAPI

Arquivo: `/docs/openapi.yaml`

✅ Pode ser importado em:

* Swagger Editor: [https://editor.swagger.io](https://editor.swagger.io)
* Redocly: [https://redocly.com](https://redocly.com)
* Postman & Insomnia

---

## 📦 Pacotes e Instrumentação

* FastAPI + Uvicorn
* SQLAlchemy
* OpenTelemetry
* OTLP Exporter
* Logging Instrumentor

✅ Observabilidade pronta para Loki / Grafana

---

## 🔐 Segurança (Sugestões)

📌 Melhorias recomendadas:

* [ ] Hash de senha com bcrypt
* [ ] Token JWT para autenticação
* [ ] Validações adicionais na entrada
* [ ] Rate limiting

---

## 🧪 Testes

Arquivo: `/tests/test_pessoas.py`
Rodar testes:

```bash
pytest -vv
```

---

## 📬 Contato / Contribuição

Pull Requests são bem-vindos! ✨

📌 Autor: *Seu nome aqui*
📌 Projeto demonstrativo de observabilidade

---

✅ **Documentação 100% pronta para GitHub!**


