import fastapi
from fastapi import responses
from fastapi import status

router = fastapi.APIRouter()


@router.get("/health")
def health_check():
    return responses.Response(status_code=status.HTTP_200_OK)
