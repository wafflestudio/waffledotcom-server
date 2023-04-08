import fastapi

from src.routers import health


def _add_routers(app: fastapi.FastAPI):
    app.include_router(health.router)


def create_app():
    app = fastapi.FastAPI()
    _add_routers(app)
    return app
