# Professional Management System - Makefile
# Simplified commands for development and deployment

.PHONY: help setup dev test test-unit test-integration clean build deploy logs stop restart

# Default target
help:
	@echo "Professional Management System - Available Commands"
	@echo "=================================================="
	@echo ""
	@echo "Development:"
	@echo "  setup          Setup development environment"
	@echo "  dev            Start development environment"
	@echo "  stop           Stop all services"
	@echo "  restart        Restart all services"
	@echo "  logs           View logs from all services"
	@echo "  logs-api       View API logs only"
	@echo ""
	@echo "Testing:"
	@echo "  test           Run all tests with coverage"
	@echo "  test-unit      Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-docker    Run tests in Docker container"
	@echo ""
	@echo "Database:"
	@echo "  migrate        Run database migrations"
	@echo "  migrate-create Create new migration"
	@echo "  db-reset       Reset database (WARNING: destroys data)"
	@echo ""
	@echo "Production:"
	@echo "  build          Build production images"
	@echo "  deploy         Deploy to production"
	@echo "  prod-logs      View production logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean          Clean up containers and volumes"
	@echo "  clean-all      Clean everything including images"
	@echo "  lint           Run code linting"
	@echo "  format         Format code"

# Development commands
setup:
	@echo "🚀 Setting up development environment..."
	./scripts/setup-dev.sh

dev:
	@echo "🔧 Starting development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "✅ Development environment started!"
	@echo "   • API: http://localhost:8000"
	@echo "   • API Docs: http://localhost:8000/docs"

stop:
	@echo "🛑 Stopping all services..."
	docker-compose -f docker-compose.dev.yml down
	docker-compose down

restart:
	@echo "🔄 Restarting services..."
	docker-compose -f docker-compose.dev.yml restart

logs:
	@echo "📋 Viewing logs from all services..."
	docker-compose -f docker-compose.dev.yml logs -f

logs-api:
	@echo "📋 Viewing API logs..."
	docker-compose -f docker-compose.dev.yml logs -f api

# Testing commands
test:
	@echo "🧪 Running all tests..."
	./scripts/run-tests.sh

test-unit:
	@echo "🧪 Running unit tests..."
	./scripts/run-tests.sh -t unit

test-integration:
	@echo "🧪 Running integration tests..."
	./scripts/run-tests.sh -t integration

test-docker:
	@echo "🧪 Running tests in Docker..."
	./scripts/run-tests.sh -d

# Database commands
migrate:
	@echo "🗃️  Running database migrations..."
	docker-compose -f docker-compose.dev.yml exec api alembic upgrade head

migrate-create:
	@echo "🗃️  Creating new migration..."
	@read -p "Enter migration message: " msg; \
	docker-compose -f docker-compose.dev.yml exec api alembic revision --autogenerate -m "$$msg"

db-reset:
	@echo "⚠️  WARNING: This will destroy all data!"
	@read -p "Are you sure? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		docker-compose -f docker-compose.dev.yml down -v; \
		rm -f data/*.db; \
		docker-compose -f docker-compose.dev.yml up -d; \
		sleep 5; \
		docker-compose -f docker-compose.dev.yml exec api alembic upgrade head; \
		echo "✅ Database reset complete!"; \
	else \
		echo "❌ Database reset cancelled."; \
	fi

# Production commands
build:
	@echo "🏗️  Building production images..."
	docker-compose build

deploy:
	@echo "🚀 Deploying to production..."
	docker-compose up -d
	@echo "✅ Production deployment complete!"

prod-logs:
	@echo "📋 Viewing production logs..."
	docker-compose logs -f

# Maintenance commands
clean:
	@echo "🧹 Cleaning up containers and volumes..."
	docker-compose -f docker-compose.dev.yml down -v
	docker-compose down -v
	docker system prune -f

clean-all:
	@echo "🧹 Cleaning everything including images..."
	docker-compose -f docker-compose.dev.yml down -v --rmi all
	docker-compose down -v --rmi all
	docker system prune -af

lint:
	@echo "🔍 Running code linting..."
	docker-compose -f docker-compose.dev.yml exec api flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	docker-compose -f docker-compose.dev.yml exec api flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "✨ Formatting code..."
	docker-compose -f docker-compose.dev.yml exec api black .
	docker-compose -f docker-compose.dev.yml exec api isort .

# Shell access
shell:
	@echo "🐚 Opening shell in API container..."
	docker-compose -f docker-compose.dev.yml exec api bash

shell-db:
	@echo "🗃️  Opening database shell..."
	docker-compose -f docker-compose.dev.yml exec postgres_dev psql -U dev_user -d professional_management_dev

# Health checks
health:
	@echo "🏥 Checking service health..."
	@curl -f http://localhost:8000/health && echo "✅ API is healthy" || echo "❌ API is not responding"

# Quick development workflow
quick-start: setup dev
	@echo "🎉 Quick start complete! Your development environment is ready."

# Install dependencies locally (for IDE support)
install-deps:
	@echo "📦 Installing dependencies locally..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

