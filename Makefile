.PHONY: up down backend frontend env-backend env-frontend

up: env-backend env-frontend backend frontend

down:
	docker compose -f inventory-system/docker-compose.yml down
	docker stop inventory-frontend 2>/dev/null || true
	docker rm inventory-frontend 2>/dev/null || true

env-backend:
	cp inventory-system/.env.example inventory-system/.env

env-frontend:
	cp inventory-frontend/.env.example inventory-frontend/.env

backend:
	docker compose -f inventory-system/docker-compose.yml up --build -d

frontend:
	docker build -t inventory-frontend ./inventory-frontend
	docker run -d -p 8080:80 --name inventory-frontend inventory-frontend
