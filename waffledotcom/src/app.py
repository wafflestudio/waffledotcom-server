import fastapi

from src.database import connection
from src.routers import health


def _add_routers(app: fastapi.FastAPI):
    app.include_router(health.router)


def _init_db_session(app: fastapi.FastAPI):
    @app.on_event("startup")
    async def startup_db_client():
        app.db_session = connection.get_db_connection().session

    @app.on_event("shutdown")
    async def shutdown_db_client():
        app.db_session.close()


def create_app():
    app = fastapi.FastAPI()
    _add_routers(app)
    _init_db_session(app)
    return app
