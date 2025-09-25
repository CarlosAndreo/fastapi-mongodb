<div align="center">

# FastAPI MongoDB <!-- omit in toc -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

[![fastapi-mongodb][fastapi-mongodb-badge]][fastapi-mongodb-url]

[Wiki](https://github.com/CarlosAndreo/fastapi-mongodb/wiki)

</div>

## :brain: About

This is a ready-to-use project template for building FastAPI applications with MongoDB as the database. It's designed to help you get started quickly with a clean architecture, pre-configured settings, and best practices for scalability and maintainability.

## Features

- JWT-based authentication.

## Roadmap

- Email verification.
- Handler exceptions.
- Refresh token.

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

Build the Docker image:

```bash
docker compose build
```

Run the Docker container:

```bash
docker compose up -d
```

The application will be available at `http://localhost:8000`.

The mongo-express UI will be available at `http://localhost:8081`.

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
[python-badge]: https://img.shields.io/badge/Python-3.13.7-blue?style=for-the-badge&logo=python&logoColor=white&labelColor=3776AB
[python-url]: https://www.python.org/downloads/release/python-3137/
[fastapi-badge]: https://img.shields.io/badge/FastAPI-0.117.1-blue?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=009688
[fastapi-url]: https://fastapi.tiangolo.com/
[mongodb-badge]: https://img.shields.io/badge/MongoDB-8.0-green?style=for-the-badge&logo=mongodb&logoColor=white&labelColor=47A248
[mongodb-url]: https://www.mongodb.com/
