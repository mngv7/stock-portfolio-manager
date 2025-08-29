FROM python:3.11.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
EXPOSE 5000

COPY start.sh .
RUN chmod +x ./start.sh

RUN useradd -m appuser
USER appuser

CMD ["./start.sh"]
