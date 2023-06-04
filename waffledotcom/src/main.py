import uvicorn

from waffledotcom.src.app import create_app


def main():
    """Entrypoint of the application."""
    fastapi_app = create_app()
    uvicorn.run(
        fastapi_app,
        host="127.0.0.1",
        port=8080,
    )


if __name__ == "__main__":
    main()
