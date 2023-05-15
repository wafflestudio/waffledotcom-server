from fastapi.routing import APIRouter

from waffledotcom.src.apis import dummy

api_router = APIRouter()
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
