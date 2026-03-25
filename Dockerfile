FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies with verbose output for debugging
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        git \
        build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt --verbose

COPY app/ ./app/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 5000

CMD ["python", "app/main.py", "--host", "0.0.0.0", "--port", "5000"]
