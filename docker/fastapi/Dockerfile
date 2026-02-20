FROM python:3.14.3-alpine

ENV PYTHONUNBUFFERED=1
ENV UV_HOME="/root/.uv"
ENV PATH="/root/.uv:${PATH}"

RUN apk add --no-cache curl gcc musl-dev libffi-dev

WORKDIR /fastapi-mongodb

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=${UV_HOME} sh

COPY . .

RUN uv sync --frozen --group dev

CMD uv run fastapi dev app/main.py --host ${BACKEND_HOST} --port ${BACKEND_PORT}
