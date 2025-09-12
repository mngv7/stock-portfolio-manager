# Dockerfile
FROM python:3.11.9-slim

WORKDIR /app

# Install Node 20
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80 5000

ARG VITE_BUILD_ENV=http://localhost:5000
ENV VITE_BUILD_ENV=${VITE_BUILD_ENV}

# Start script
COPY start.sh .
RUN chmod +x ./start.sh

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["./start.sh"]
