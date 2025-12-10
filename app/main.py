from contextlib import asynccontextmanager

from core.config import settings
from core.logger import get_logger, setup_logging

setup_logging(log_level=settings.LOG_LEVEL, use_json=settings.LOG_JSON_FORMAT)
logger = get_logger(name=__name__)

# ruff: noqa: E402
from core.constants import API_PREFIX
from database.mongodb import mongodb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.logging import LoggingMiddleware
from routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event to connect to MongoDB
    """
    await mongodb.connect()
    yield
    await mongodb.disconnect()


app = FastAPI(
    title="FastAPI MongoDB",
    description="Ready-to-use FastAPI template with MongoDB.",
    version="1.0",
    docs_url=f"{API_PREFIX}/docs",
    redoc_url=f"{API_PREFIX}/redoc",
    openapi_url=f"{API_PREFIX}/openapi.json",
    routes=router.routes,
    lifespan=lifespan,
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    swagger_ui_parameters={
        "syntaxHighlight": {"theme": "obsidian"},
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none",
        "displayRequestDuration": True,
        "filter": True,
        "persistAuthorization": True,
        "operationsSorter": "method",
        "tagsSorter": "alpha",
        "showCommonExtensions": True,
        "tryItOutEnabled": True,
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(middleware_class=LoggingMiddleware)
