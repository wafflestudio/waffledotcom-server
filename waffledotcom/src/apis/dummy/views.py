from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_dummy():
    return {"dummy": "dummy"}
