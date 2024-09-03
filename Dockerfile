FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
