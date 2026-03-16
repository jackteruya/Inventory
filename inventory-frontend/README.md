# Inventory Frontend (React)

Frontend em React + Vite para o desafio técnico de estoque.

## Funcionalidades

- Consulta do healthcheck da API
- Listagem de itens em estoque
- Ordenação por nome, quantidade ou última atualização
- Adição de estoque
- Baixa de estoque por item
- Indicador visual para itens com estoque crítico (`quantity < 5`)

## Requisitos

- Node.js 20+
- API backend rodando localmente

## Configuração

Crie um arquivo `.env` com base no `.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Rodando localmente

```bash
npm install
npm run dev
```

A aplicação ficará disponível em `http://localhost:5173`.

## Build

```bash
npm run build
npm run preview
```

## Integração com o backend

Endpoints utilizados:

- `GET /health/`
- `GET /api/inventory/`
- `POST /api/inventory/`
- `DELETE /api/inventory/{id}/`

## Docker

```bash
docker build -t inventory-frontend .
docker run -p 8080:80 inventory-frontend
```
