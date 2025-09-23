# FloatChat Dockerfile - Multi-stage build for Frontend + Backend
# Supports both development and production deployments

# === Stage 1: Frontend Build ===
FROM node:18-alpine as frontend-builder
WORKDIR /app

# Install frontend dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code and build
COPY public/ ./public/
COPY src/ ./src/
RUN npm run build

# === Stage 2: Frontend Development (optional) ===
FROM node:18-alpine as frontend-dev
WORKDIR /app

# Install all dependencies (including dev dependencies)
COPY package*.json ./
RUN npm install

# Copy source code
COPY public/ ./public/
COPY src/ ./src/

# Expose development server port
EXPOSE 3000

# Start development server
CMD ["npm", "start"]

# === Stage 3: Python Base Environment ===
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# === Stage 4: Dependencies Installation ===
FROM base as deps

# Copy Python requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# === Stage 5: Production API Server ===
FROM deps as production

# Copy application code
COPY lightweight_pipeline.py .
COPY lightweight_plot_generator.py .
COPY sql_query_generator.py .
COPY floatchat_bot.py .
COPY api_server.py .

# Copy frontend build (from frontend-builder stage)
COPY --from=frontend-builder /app/build ./build

# Create necessary directories
RUN mkdir -p plots logs

# Copy environment files
COPY .env* ./

# Expose API port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Start API server
CMD ["python", "api_server.py"]

# === Stage 6: Development Environment ===
FROM deps as development

# Install additional development tools
RUN pip install ipython jupyter

# Copy all source files for development
COPY . .

# Create directories
RUN mkdir -p plots logs

# Expose both API and frontend ports
EXPOSE 5000 3000

# Development startup script
CMD ["python", "api_server.py"]