.PHONY: install dev run migrate test clean

install:
	uv sync

dev:
	uv run uvicorn app.main:app --port 8000

run:
	uv run uvicorn app.main:app --port 8000

migrate:
	uv run alembic upgrade head

migrate-create:
	uv run alembic revision --autogenerate -m "$(msg)"

migrate-down:
	uv run alembic downgrade -1

test:
	uv run pytest

clean:
	rm -f database.db
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies with uv"
	@echo "  make dev          - Run development server with uv"
	@echo "  make run          - Run server with uv"
	@echo "  make migrate      - Run database migrations"
	@echo "  make migrate-create msg='message' - Create new migration"
	@echo "  make migrate-down - Rollback last migration"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean database and cache files"
