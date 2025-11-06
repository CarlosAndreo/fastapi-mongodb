from contextlib import asynccontextmanager

from database.mongodb import mongodb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    docs_url="/",
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
