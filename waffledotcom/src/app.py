import fastapi

from src.database import connection
from waffledotcom.src.database.connection import DBSessionFactory


def _add_routers(app: fastapi.FastAPI):
    app.include_router(health.router)



def register_shutdown_event(app: fastapi.FastAPI):
    @app.on_event("shutdown")
    def on_shutdown():
        DBSessionFactory().teardown()

    return on_shutdown()


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI()
    _add_routers(app)
    register_shutdown_event(app)
    return app
