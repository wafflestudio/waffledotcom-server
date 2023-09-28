from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from waffledotcom.src.apps.router import api_router
from waffledotcom.src.database.connection import DBSessionFactory
from waffledotcom.src.settings import settings


def _add_middlewares(app: FastAPI):
    if settings.is_dev:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def _add_routers(app: FastAPI):
    app.include_router(router=api_router)


def _register_shutdown_event(app: FastAPI):
    @app.on_event("shutdown")
    def on_shutdown():
        DBSessionFactory().teardown()

    return on_shutdown


def create_app() -> FastAPI:
    app = FastAPI(
        title="waffledotcom-server",
        debug=settings.is_dev,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    _add_middlewares(app)
    _add_routers(app)
    _register_shutdown_event(app)
    return app
