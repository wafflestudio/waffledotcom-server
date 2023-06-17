from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1/dummy", tags=["dummy"])


@v1_router.get("")
def get_dummy():
    return {"dummy": "dummy"}
