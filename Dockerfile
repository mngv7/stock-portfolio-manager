FROM python:3.11.9-slim

WORKDIR /app

# Install Node.js 20
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app code
COPY . .

# Expose ports
EXPOSE 8080
EXPOSE 5000

# Copy start script
COPY start.sh .
RUN chmod +x ./start.sh

# Create non-root user and give permissions
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Start both frontend + backend
CMD ["./start.sh"]
