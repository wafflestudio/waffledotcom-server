import fastapi

router = fastapi.APIRouter()


@router.get("/health")
def health_check():
    return fastapi.responses.Response(status_code=fastapi.status.HTTP_200_OK)
