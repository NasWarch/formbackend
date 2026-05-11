.PHONY: dev build up down logs migrate migration shell deploy backup clean

# Development
dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose restart

# Database
migrate:
	cd backend && alembic upgrade head

migration:
	cd backend && alembic revision --autogenerate -m "$(name)"

downgrade:
	cd backend && alembic downgrade -1

# Shell
shell:
	cd backend && python -c "\
from app.core.database import SessionLocal; \
db = SessionLocal(); \
print('DB session ready'); \
db.close()"

# Deployment
deploy:
	bash scripts/deploy.sh

backup:
	bash scripts/backup-db.sh

# Cleanup
clean-pyc:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-cache:
	rm -rf .pytest_cache backend/.pytest_cache

clean: clean-pyc clean-cache
