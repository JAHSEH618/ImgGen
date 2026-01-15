# Img Gen Backend Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-flexible.txt requirements-core.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    (pip install --no-cache-dir -r requirements-core.txt || \
     pip install --no-cache-dir -r requirements-flexible.txt)

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p upload generated

# Expose ports
EXPOSE 8088 10086

# Environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:10086/list && curl -f http://localhost:8088/list_generated || exit 1

# Run both services using the service manager
CMD ["python", "__init__.py"]