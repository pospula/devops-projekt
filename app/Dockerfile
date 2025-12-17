# ==========================================
# ETAP 1: BUILDER
# ==========================================
FROM python:3.10-slim AS builder

# python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system updates and stuff
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# python reqs
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy code
COPY src/ ./src
COPY tests/ ./tests


# ==========================================
# ETAP 2: TESTER
# ==========================================
FROM builder AS tester

# make /app a main module
ENV PYTHONPATH=/app

# run tests
RUN pytest