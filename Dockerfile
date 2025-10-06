FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Make uv to use system python
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with `uv sync` from .lock file (no `uv pip install` - slower)
RUN uv sync --frozen --no-dev

# Copy project
COPY . ./

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]