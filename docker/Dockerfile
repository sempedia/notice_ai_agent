# Use the official Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    POETRY_VERSION=2.1.2 \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential git libffi-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry in a non-root directory
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION \
 && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry \
 && poetry --version

# Create non-root user
RUN useradd --create-home appuser

# Set working directory
WORKDIR /app

# Ensure directory is owned by appuser
RUN chown -R appuser:appuser /app

# Copy files and set ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Install dependencies
RUN poetry lock \
 && poetry install --no-root --no-interaction --no-ansi --with dev

# Show installed packages
RUN poetry show --tree

# Show Python version
RUN poetry run python --version

# Default command
CMD ["poetry", "run", "python"]
