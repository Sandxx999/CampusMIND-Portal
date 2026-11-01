# ------------------------------------------------------------------------------
# Stage 1: Build the React Frontend
# ------------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci || npm install

COPY frontend/ ./
RUN npm run build

# ------------------------------------------------------------------------------
# Stage 2: Python Backend & Unified Monolith Runner
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS runner
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python backend dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend source code and seed data
COPY backend/ ./backend/
COPY data/ ./data/

# Copy built frontend assets from Stage 1 into frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Set environment defaults
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=development
ENV DEMO_MODE=true
ENV PORT=8000
ENV CORS_ORIGINS="http://localhost:5173,http://localhost:3000,http://localhost:8000,https://onrender.com"

EXPOSE 8000

# Start Uvicorn on Render's dynamic PORT
CMD ["sh", "-c", "cd backend && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
