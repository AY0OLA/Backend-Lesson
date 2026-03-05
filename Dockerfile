FROM python:3.10-slim

WORKDIR /usr/src/app

# This one go prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./

# Na here we Dey upgrade pip and we Dey increase timeout and retries
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=200 --retries=10 -r requirements.txt

COPY . .

# Use shell form so $PORT go expand
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}