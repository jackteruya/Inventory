.PHONY: up backend frontend env-backend env-frontend

up: env-backend env-frontend backend frontend

env-backend:
	cp inventory-system/.env.example inventory-system/.env

env-frontend:
	cp inventory-frontend/.env.example inventory-frontend/.env

backend:
	docker compose -f inventory-system/docker-compose.yml up --build -d

frontend:
	docker build -t inventory-frontend ./inventory-frontend
	docker run -d -p 8080:80 --name inventory-frontend inventory-frontend
