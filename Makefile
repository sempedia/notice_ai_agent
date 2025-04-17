.PHONY: install lock build test lint format precommit check init update-hooks ci \
	format-local lint-local test-local check-local

UID := $(shell id -u)
GID := $(shell id -g)

# ==============================
# 🧪 LOCAL DEVELOPMENT COMMANDS
# ==============================

# Install the project dependencies (including dev dependencies)
install:
	poetry install --with dev

# Regenerate the poetry.lock file (without updating dependencies)
lock:
	poetry lock --regenerate

# Fix permissions locally before formatting
format-local:
	sudo chown -R $$(id -u):$$(id -g) tests/
	chmod -R u+rw tests/
	poetry run black .
	poetry run isort .

# Run linters locally (like in CI)
lint-local:
	poetry run black . --check
	poetry run isort . --check-only
	poetry run flake8 . --exclude=.venv/
	poetry run mypy .
	poetry run ruff check . --config pyproject.toml

# Run tests locally
test-local:
	poetry run pytest --maxfail=1 --disable-warnings

# Run pre-commit checks locally
check-local:
	poetry run pre-commit run --all-files --show-diff-on-failure

# ==============================
# 🐳 DOCKERIZED CI-LIKE COMMANDS
# ==============================

# Build the Docker image (includes both main and dev dependencies)
build:
	docker buildx build --no-cache -f docker/Dockerfile -t langgraph .

# Run tests using Docker
test: build
	@docker run --rm -u $(UID):$(GID) -v $(PWD):/app -w /app -e PYTHONPATH=/app langgraph sh -c "\
	poetry install --no-root --no-interaction --with dev --quiet && \
	poetry run pytest --maxfail=1 --disable-warnings"

# Run linters using Docker
lint: build
	@docker run --rm -u $(UID):$(GID) -v $(PWD):/app -w /app -e PYTHONPATH=/app langgraph sh -c "\
	poetry install --no-root --no-interaction --with dev && \
	poetry run black . --check && \
	poetry run isort . --check-only && \
	poetry run flake8 . --exclude=.venv/ && \
	poetry run mypy . && \
	poetry run ruff check . --config pyproject.toml"

# Format the code using Docker
format: build
	@docker run --rm -u $(UID):$(GID) \
		-v $(PWD):/app -w /app -e PYTHONPATH=/app langgraph sh -c "\
		poetry install --no-root --no-interaction --with dev --quiet && \
		poetry run black . && \
		poetry run isort ."

# Add __init__.py files automatically where needed
init:
	@docker run --rm -u $(UID):$(GID) -v $(PWD):/app -w /app -e PYTHONPATH=/app langgraph sh -c "\
		poetry run python scripts/add_init_files.py"

# Update pre-commit hooks to their latest versions
update-hooks: build
	@echo "Updating pre-commit hooks..."
	@docker run --rm -v $(PWD):/app -w /app langgraph \
		poetry run pre-commit autoupdate

# Run pre-commit hooks (formats and auto-updates first)
precommit: update-hooks format build
	@docker run --rm -u $(UID):$(GID) \
		-v $(PWD):/app -w /app -e PYTHONPATH=/app langgraph sh -c "\
		poetry install --no-root --no-interaction --with dev --quiet && \
		poetry run pre-commit run --all-files"

# Check pre-commit hooks without formatting
check: build
	@docker run --rm -v $(PWD):/app -w /app langgraph \
		poetry run pre-commit run --all-files --show-diff-on-failure

# Full CI pipeline (build, test, lint, pre-commit checks)
ci: build test lint check
