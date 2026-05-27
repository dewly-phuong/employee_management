# Giai đoạn 1: Xây dựng (Builder)
FROM python:3.13-slim AS builder

# Thiết lập các biến môi trường cho Python và Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.4.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Thêm Poetry vào PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Cài đặt các công cụ hệ thống cần thiết và Poetry
RUN apt-get update && apt-get install --no-install-recommends -y curl \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copy các file quản lý phụ thuộc
COPY pyproject.toml poetry.lock ./

# Chỉ cài đặt các thư viện cần thiết (loại bỏ group dev nếu có)
RUN poetry lock && poetry install --only main --no-root

# Giai đoạn 2: Chạy ứng dụng (Runtime)
FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy các gói thư viện đã cài đặt từ builder
COPY --from=builder /usr/local /usr/local

# Copy mã nguồn của dự án
COPY . .

# Chạy ứng dụng FastAPI bằng Uvicorn
EXPOSE 8000
CMD ["uvicorn", "src.employee_management.main:app", "--host", "0.0.0.0", "--port", "8000"]