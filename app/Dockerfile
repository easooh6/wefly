FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements*.txt .

RUN pip install --no-cache-dir -r requirements.txt -r requirements-test.txt

COPY . .

RUN mkdir -p logs

EXPOSE 8000

CMD ["python", "run.py"]