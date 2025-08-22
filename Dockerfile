# Use slim Python base
FROM python:3.11-slim AS base

# Install build deps in a builder stage
FROM base AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final lightweight image
FROM base
WORKDIR /app

# Install runtime dependencies only (no compilers)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Run with Gunicorn (expand PORT properly)
CMD ["sh", "-c", "gunicorn BrillianBengaluru.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
