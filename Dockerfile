FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 5000
EXPOSE 8080

COPY start.sh .
RUN chmod +x /start.sh
CMD ["./start.sh"]
