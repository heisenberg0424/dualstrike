FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/YOUR_USERNAME/YOUR_REPO /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD git pull && pip install -q -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8000
