import uvicorn

from waffledotcom.src.app import create_app

# Entrypoint for Docker container.
app = create_app()


def main():
    # Entrypoint for manual execution.
    uvicorn.run(
        "waffledotcom.src.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    main()
