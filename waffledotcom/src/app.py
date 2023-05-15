import fastapi

from waffledotcom.src.apis.router import api_router
from waffledotcom.src.database.connection import DBSessionFactory


def add_routers(app: fastapi.FastAPI):
    app.include_router(router=api_router, prefix="/api")


def register_shutdown_event(app: fastapi.FastAPI):
    @app.on_event("shutdown")
    def on_shutdown():
        DBSessionFactory().teardown()

    return on_shutdown()


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    add_routers(app)
    register_shutdown_event(app)
    return app
