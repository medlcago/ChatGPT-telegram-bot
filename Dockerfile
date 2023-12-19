FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .

ENV PYTHONPATH=/app

CMD ["python", "bot/app.py"]