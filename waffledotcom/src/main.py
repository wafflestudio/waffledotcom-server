import uvicorn

from src import app as app_factory


def main():
    """Entrypoint of the application."""
    fastapi_app = app_factory.create_app()
    uvicorn.run(
        fastapi_app,
        host="127.0.0.1",
        port="8080",
    )


if __name__ == "__main__":
    main()
