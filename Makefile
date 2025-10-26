.PHONY: help uv dev build up down restart logs migrate init-db

# Hiển thị các lệnh có sẵn
help:
	@echo "Makefile commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

uv: ## Install dependencies using uv
	uv pip install -r <(uv pip compile pyproject.toml --without-hashes)

init-alembic: ## Initialize Alembic (run only once)
	# check if alembic.ini exists
	if [ ! -f alembic.ini ]; then \
		alembic init alembic; \
		sed -i '' 's|sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = postgresql+psycopg2://$(POSTGRES_USER:-admin):$(POSTGRES_PASSWORD:-admin)@db:5432/$(POSTGRES_DB:-procondb)|g' alembic.ini; \
		echo "Alembic initialized and alembic.ini configured."; \
	else \
		echo "alembic.ini already exists. Skipping initialization."; \
	fi

dev: ## Start local dev server with uvicorn
	uvicorn app.main:app --reload

build: ## Build Docker image
	docker compose build

up: ## Compose up in detached mode
	docker compose up -d

down: ## Compose down and remove volumes
	docker compose down

clean: ## Remove all containers, volumes, images, and orphans # --rmi all --remove-orphans
	docker compose down -v 

restart: ## Restart the docker containers
	docker compose down
	docker compose up -d

exec: ## Exec into the api container
	docker compose exec procon-api /bin/bash

logs: ## Tail application logs
	tail -f logs/system.log

migrate: ## Run database migrations (alembic)
	alembic revision --autogenerate -m "auto"
	alembic upgrade head

init-db: ## Create tables and ingest initial data (via app startup event)
	docker compose run api python -c 'import asyncio; from app.main import startup_event; asyncio.run(startup_event())'
