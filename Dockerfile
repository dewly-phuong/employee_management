# Stage 1: Build stage
FROM python:3.14-slim AS builder

WORKDIR /app

# Cài đặt Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==2.4.0

# Copy file cấu hình poetry
COPY pyproject.toml poetry.lock ./

# Cài đặt dependencies
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Stage 2: Runtime stage
FROM python:3.14-slim AS runtime

WORKDIR /app

# Copy môi trường ảo (.venv) từ stage builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy mã nguồn
COPY . .

# Chạy FastAPI
CMD ["/app/.venv/bin/python", "-m", "uvicorn", "employee_management.main:app", "--host", "0.0.0.0", "--port", "8000"]