FROM python:3.13.3-slim

ENV UV_HOME="/root/.uv"
ENV PATH="/root/.uv:${PATH}"

EXPOSE 8000

RUN apt-get update && apt-get install -y curl

WORKDIR /fastapi-mongodb

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="${UV_HOME}" sh

COPY . .

RUN uv sync

CMD ["uv", "run", "fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]
