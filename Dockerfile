FROM python:3.12-slim

WORKDIR /app

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY app alembic alembic.ini ./

RUN mkdir -p storages/questions logs
RUN useradd --create-home procon
USER procon

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]