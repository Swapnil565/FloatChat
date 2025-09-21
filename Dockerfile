# FloatChat - Ocean Data Query System
# Multi-stage Docker build for production deployment

# Stage 1: Base Python environment
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    postgresql-client \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash floatchat
RUN chown -R floatchat:floatchat /app

# Stage 2: Dependencies installation
FROM base as dependencies

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM dependencies as application

# Switch to non-root user
USER floatchat

# Copy application code
COPY --chown=floatchat:floatchat . .

# Create necessary directories
RUN mkdir -p logs data

# Copy environment configuration
COPY --chown=floatchat:floatchat .env.docker .env

# Expose port for Flask API
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

# Default command - can be overridden
CMD ["python", "api_server.py"]

# Optional: Add labels for container metadata
LABEL maintainer="FloatChat Team"
LABEL version="1.0"
LABEL description="Ocean Data Query System with Natural Language Processing"
LABEL project="FloatChat"