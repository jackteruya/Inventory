# Sistema de Gerenciamento de Estoque

Aplicação fullstack de gerenciamento de estoque composta por uma API REST e uma interface web.

## Visão geral

O sistema permite adicionar e remover itens do estoque, listar o inventário com ordenação customizável e identificar itens em nível crítico. As operações de escrita disparam tarefas assíncronas via Celery, garantindo consistência sob carga concorrente.

## Estrutura do repositório

```
inventory/
├── inventory-system/     # Backend — API REST
└── inventory-frontend/   # Frontend — interface web
```

## Stack

### Backend — [`inventory-system`](./inventory-system/README.md)

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Linguagem principal |
| FastAPI | Framework web assíncrono |
| SQLAlchemy (async) | ORM com suporte a `async/await` |
| PostgreSQL | Banco de dados relacional |
| Alembic | Migrations |
| Celery | Fila de tarefas assíncronas |
| RabbitMQ | Message broker |
| Docker / Docker Compose | Containerização |

### Frontend — [`inventory-frontend`](./inventory-frontend/README.md)

| Tecnologia | Uso |
|---|---|
| React 18 | Biblioteca de UI |
| TypeScript | Tipagem estática |
| Vite | Bundler e dev server |
| Docker | Containerização |

## Como rodar

### Pré-requisitos

- Docker e Docker Compose instalados
- `make` disponível no sistema

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Inventory
```

### 2. Suba tudo de uma vez (atalho)

```bash
make up
```

Esse comando gera os `.env` de cada subprojeto a partir dos `.env.example` e sobe o backend e o frontend na sequência. Edite os `.env` antes se precisar de configurações customizadas.

---

Ou, se preferir rodar cada etapa separadamente:

### Configure as variáveis de ambiente

```bash
make env-backend
make env-frontend
```

Isso copia os arquivos `.env.example` para `.env` em cada subprojeto. Edite-os se necessário antes de subir os serviços.

### 3. Suba o backend

```bash
make backend
```

Isso builda e sobe em background: API, worker Celery, PostgreSQL e RabbitMQ.

Serviços disponíveis:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- RabbitMQ: `http://localhost:15672`

### 4. Suba o frontend

```bash
make frontend
```

Interface disponível em `http://localhost:8080`.

> Consulte o README de cada parte para detalhes de configuração, variáveis de ambiente e execução de testes:
> - [Backend](./inventory-system/README.md)
> - [Frontend](./inventory-frontend/README.md)
