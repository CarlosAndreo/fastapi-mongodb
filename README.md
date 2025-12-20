<div align="center">

# FastAPI MongoDB <!-- omit in toc -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![Coverage][coverage-shield]][coverage-url]

<!-- [![fastapi-mongodb][fastapi-mongodb-badge]][fastapi-mongodb-url] -->

</div>

## :brain: About

This is a ready-to-use project template for building FastAPI applications with MongoDB as the database. It's designed to help you get started quickly with a clean architecture, pre-configured settings, and best practices for scalability and maintainability.

## :file_folder: Project Structure

```
fastapi-mongodb/
├── app/
│   ├── core/                # Core configuration and utilities
│   │   ├── config.py        # Environment variables and configuration
│   │   ├── constants.py     # Application constants
│   │   ├── jwt.py           # JWT token handling
│   │   ├── logger.py        # Logging configuration
│   │   └── security.py      # Security utilities
│   ├── database/
│   │   ├── init-db.js       # MongoDB initialization script
│   │   └── mongodb.py       # MongoDB connection and configuration
│   ├── middlewares/
│   │   └── logging.py       # Logging middleware
│   ├── repositories/
│   │   └── user.py          # User data access layer
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── me.py            # Current user endpoints
│   ├── schemas/
│   │   └── user.py          # Pydantic user schemas
│   ├── services/
│   │   ├── auth.py          # Authentication business logic
│   │   └── user.py          # User business logic
│   └── main.py              # Application entry point
├── docker/
│   └── fastapi/
│       └── Dockerfile       # FastAPI Docker image
├── tests/
│   ├── conftest.py          # Pytest configuration
│   ├── test_auth.py         # Authentication tests
│   └── test_me.py           # User endpoints tests
├── .env.template            # Environment variables template
├── docker-compose.yaml      # Docker Compose configuration
├── pyproject.toml           # Project dependencies and configuration
├── pytest.toml              # Pytest configuration
└── ruff.toml                # Linter configuration
```

## Features

- JWT-based authentication.
- Refresh token.
- Middleware.
- Tests with pytest.
- Log handler.
- Indexes to MongoDB.

## Roadmap

- Email verification.
- Handler exceptions.

## :hammer_and_wrench: Stack
- [![Python][python-badge]][python-url] - Programming language.
- [![FastAPI][fastapi-badge]][fastapi-url] - Python framework for web applications to expose the API.
- [![MongoDB][mongodb-badge]][mongodb-url] - NoSQL database.

## :rocket: Getting Started Locally

Install Docker following the instructions for your operating system:

- [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

- [Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

- [MacOS](https://docs.docker.com/desktop/install/mac-install/)

Clone the repository:

```bash
git clone https://github.com/CarlosAndreo/fastapi-mongodb.git
cd fastapi-mongodb
```

Create the `.env` file from the template:

```bash
cp .env.template .env
```

> [!NOTE]
> Edit the `.env` file and update the values according to your needs. Make sure to set a strong `SECRET_KEY` (you can generate one with `openssl rand -hex 32`).

Build the Docker image:

```bash
docker compose build
```

Run the Docker container:

```bash
docker compose up -d
```

The application will be available at `http://localhost:8000/api/v1/docs`.

The mongo-express UI will be available at `http://localhost:8081`.

## :test_tube: Test

> [!WARNING] 
> When run the tests, the database is cleaned.

To test the application, access to the fastapi container:
```sh
docker exec -it fastapi-mongodb sh
```
Finally, execute:
```sh
uv run pytest
```

## Contributors <!-- omit in toc -->

<a href="https://github.com/CarlosAndreo/fastapi-mongodb/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=CarlosAndreo/fastapi-mongodb" />
</a>

[fastapi-mongodb-badge]: https://img.shields.io/github/v/release/CarlosAndreo/fastapi-mongodb?label=fastapi-mongodb&color=blue
[fastapi-mongodb-url]: https://github.com/CarlosAndreo/fastapi-mongodb/releases/latest
[contributors-shield]: https://img.shields.io/github/contributors/CarlosAndreo/fastapi-mongodb.svg?style=for-the-badge
[contributors-url]: https://github.com/CarlosAndreo/fastapi-mongodb/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/CarlosAndreo/fastapi-mongodb.svg?style=for-the-badge
[forks-url]: https://github.com/CarlosAndreo/fastapi-mongodb/network/members
[stars-shield]: https://img.shields.io/github/stars/CarlosAndreo/fastapi-mongodb.svg?style=for-the-badge
[stars-url]: https://github.com/CarlosAndreo/fastapi-mongodb/stargazers
[issues-shield]: https://img.shields.io/github/issues/CarlosAndreo/fastapi-mongodb.svg?style=for-the-badge
[issues-url]: https://github.com/CarlosAndreo/fastapi-mongodb/issues
[license-shield]: https://img.shields.io/github/license/CarlosAndreo/fastapi-mongodb.svg?style=for-the-badge
[license-url]: https://github.com/CarlosAndreo/fastapi-mongodb/blob/main/LICENSE
[python-badge]: https://img.shields.io/badge/Python-3.14.0-blue?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB
[python-url]: https://www.python.org/downloads/release/python-3140/
[fastapi-badge]: https://img.shields.io/badge/FastAPI-0.125.0-blue?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=009688
[fastapi-url]: https://fastapi.tiangolo.com/
[mongodb-badge]: https://img.shields.io/badge/MongoDB-8.2-green?style=for-the-badge&logo=mongodb&logoColor=white&labelColor=47A248
[mongodb-url]: https://www.mongodb.com/
[coverage-shield]: https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/CarlosAndreo/850532d425504682573f5b24d17fdf87/raw/coverage.json&style=for-the-badge
[coverage-url]: https://github.com/CarlosAndreo/fastapi-mongodb/actions/workflows/pytest.yaml
