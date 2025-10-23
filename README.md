# 🛰️ FastAPI Observability Project

> 🔍 Um projeto completo de **observabilidade** com **FastAPI**, **OpenTelemetry** e **Grafana LGTM (Loki, Grafana, Tempo, Mimir)**.  
> Permite monitorar **logs**, **traces** e **métricas** de uma aplicação Python em tempo real, com dashboards personalizados no Grafana.

---

## 📘 Visão Geral

Este projeto demonstra como instrumentar uma aplicação **FastAPI** com **OpenTelemetry**, exportando observabilidade para a stack **Grafana LGTM**, composta por:
- **Grafana** — Visualização de dashboards;
- **Loki** — Armazenamento e consulta de logs;
- **Tempo** — Coleta e rastreamento de traces;
- **Mimir** — Métricas de aplicação.

O objetivo é centralizar tudo em um único painel para diagnóstico e monitoramento de desempenho.

---

## 🧩 Tecnologias Utilizadas

| Tecnologia | Função | Porta |
|-------------|--------|-------|
| **FastAPI** | API principal instrumentada com OpenTelemetry | `8000` |
| **SQLAlchemy + SQLite** | ORM e persistência de dados | — |
| **OpenTelemetry SDK** | Coleta e exporta traces, logs e métricas | — |
| **Grafana LGTM Stack** | Visualização e armazenamento dos dados de observabilidade | `3000` |
| **Loki** | Coleta e busca de logs | `3100` |
| **Promtail** | Envio de logs dos containers para o Loki | `9080` |
| **Tempo** | Armazenamento e correlação de traces | — |

---

## 🧱 Arquitetura

```text
 ┌────────────────────────────┐
 │        FastAPI App         │
 │  (OpenTelemetry SDK)       │
 └───────────┬────────────────┘
             │ OTLP/gRPC
             ▼
 ┌────────────────────────────┐
 │   Grafana LGTM Stack       │
 │ (Grafana + Loki + Tempo +  │
 │  Mimir + Promtail)         │
 └───────────┬────────────────┘
             ▼
     Dashboards e Alertas

```

## 📁 Estrutura do Projeto  

```text
user_opentelemetry_observabilidade/
│
├── app/
│   ├── app.py               # Aplicação principal FastAPI
│   ├── database.py          # Configuração do SQLAlchemy
│   ├── models.py            # Modelo Pessoa
│   ├── schemas.py           # Schemas Pydantic
│   ├── routes/
│   │   └── pessoa_routes.py # Rotas CRUD
│   └── __init__.py
│
├── tests/
│   ├── conftest.py          # Banco temporário para pytest
│   ├── test_main.py         # Teste do /ping
│   └── test_users.py        # Testes CRUD
│
├── docker-compose.yml       # Stack Grafana + Loki + Promtail
├── promtail-config.yaml     # Configuração do Promtail
├── .env                     # Variáveis OpenTelemetry
├── requirements.txt         # Dependências
└── README.md                # Este arquivo


