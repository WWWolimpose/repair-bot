FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY final_bot_ready.py .
COPY runtime.txt .

CMD ["python3", "final_bot_ready.py"]
