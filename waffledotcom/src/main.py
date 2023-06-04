import uvicorn

from waffledotcom.src.app import create_app

app = create_app()


def main():
    """Entrypoint of the application."""
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
    )


if __name__ == "__main__":
    main()
