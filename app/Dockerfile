FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade --no-cache-dir -r /tmp/requirements.txt

COPY . /app

ARG VERSION=0.0.0

RUN sed -i "s/0.0.0/$VERSION/" /app/src/__init__.py

EXPOSE 80

ARG BUILD_MODE=production

ENV BUILD_MODE=$BUILD_MODE
CMD alembic upgrade head && \
    if [ "$BUILD_MODE" = "development" ]; then \
        uvicorn src.main:app --host 0.0.0.0 --port 80 --reload; \
    else \
        gunicorn --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 src.main:app; \
    fi
