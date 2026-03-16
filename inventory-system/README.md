# Sistema de Estoque

Implementação com FastAPI + PostgreSQL + Celery + RabbitMQ para o desafio técnico.

## Principais decisões

- **API e acesso ao banco assíncronos**: uso de `async/await` com SQLAlchemy async para I/O não-bloqueante.
- **Arquitetura limpa (Clean Architecture)**: separação em camadas — domain, application, infrastructure, api.
- **Bloqueio pessimista** com `SELECT ... FOR UPDATE` para garantir integridade do estoque sob concorrência.
- **Tarefa assíncrona após o commit**: as alterações de estoque são persistidas primeiro, depois um evento é publicado no Celery.
- **Normalização de nomes**: nomes como `Açaí`, `acai`, `AÇAÍ` são mapeados para o mesmo `identifier`.

## Arquitetura

```text
app/
├── api/                  # Rotas, schemas, tratamento de erros
├── application/          # Casos de uso e interfaces de serviços
├── domain/               # Entidades, exceções, repositórios (interfaces), serviços de domínio
├── infrastructure/       # Banco de dados, mensageria, normalizadores (implementações concretas)
│   └── db/
│       └── migrations/   # Migrations Alembic
└── main.py
```

### Fluxo de uma requisição

1. Requisição chega na rota FastAPI.
2. Rota chama o caso de uso correspondente.
3. Caso de uso abre uma unidade de trabalho (Unit of Work / transação).
4. Repositório lê e escreve via SQLAlchemy.
5. Após o commit bem-sucedido, uma tarefa Celery é despachada de forma assíncrona (fire-and-forget).

## Estratégia de concorrência

O desafio exige que os endpoints suportem múltiplas requisições simultâneas com integridade final do estoque verificada.

A operação crítica é a adição e remoção de estoque. Ambas utilizam:

```sql
SELECT * FROM inventory_items WHERE identifier = :identifier FOR UPDATE;
SELECT * FROM inventory_items WHERE id = :id FOR UPDATE;
```

Isso bloqueia a linha dentro da transação.

### Por que isso previne race conditions

Sem bloqueio:
- Requisição A lê quantidade `10`
- Requisição B lê quantidade `10`
- Ambas validam e escrevem
- Estoque final pode ficar inconsistente ou negativo

Com `FOR UPDATE`:
- Requisição A bloqueia a linha
- Requisição B aguarda
- Requisição A faz commit com a quantidade atualizada
- Requisição B lê o novo valor e procede com sucesso ou falha de forma segura

### Race condition em novos itens

Para inserções simultâneas do mesmo item (quando ele ainda não existe), utiliza-se um **UPSERT**:

```sql
INSERT INTO inventory_items (...) ON CONFLICT (identifier) DO NOTHING;
```

Isso garante que apenas um INSERT vence, eliminando a possibilidade de `UniqueViolationError` sob carga.

## Endpoints

### Adicionar estoque
`POST /api/inventory/`

```json
{
  "name": "Açaí",
  "quantity": 10
}
```

Retorno `202 Accepted`:
```json
{
  "id": "uuid",
  "identifier": "acai"
}
```

### Listar itens
`GET /api/inventory/`

Parâmetros opcionais:
- `order_by=name|quantity|last_updated`
- `direction=asc|desc`

Ordenação padrão (sem parâmetros):
1. Quantidade abaixo de 5 (crítico) primeiro
2. `last_updated` DESC
3. `name` ASC

### Consultar item
`GET /api/inventory/{id}/`

### Remover estoque
`DELETE /api/inventory/{id}/`

```json
{
  "quantity": 2
}
```

Respostas:
- `202` operação aceita
- `404` item não encontrado
- `409` estoque insuficiente
- `400` entrada inválida

### Health check
`GET /health/`

## Executando com Docker

```bash
docker compose up --build
```

Serviços disponíveis:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Gerenciamento RabbitMQ: `http://localhost:15672`

## Variáveis de ambiente

Consulte o arquivo `.env.example`.

## Executando as migrations manualmente

```bash
docker compose exec api alembic upgrade head
```

## Executando os testes

```bash
uv pip install -r requirements-dev.txt
pytest
```

## Lint e formatação

```bash
# verificar problemas
ruff check .

# corrigir automaticamente
ruff check . --fix

# formatar código
ruff format .
```

O pre-commit está configurado para rodar `ruff check` e `ruff format` automaticamente antes de cada commit:

```bash
pre-commit install
```

## Sobre a tarefa assíncrona

A atualização do estoque em si **não** é executada pelo Celery.

Fluxo correto:
- Transação da API atualiza o estoque de forma síncrona (async I/O)
- Commit é confirmado
- Tarefa Celery é publicada na fila
- Worker simula atraso (1–5s), falha aleatória (50%) e retry com backoff (3s, 6s, 12s)

Isso está alinhado com o enunciado do desafio: *a operação também deve disparar uma tarefa assíncrona*.
