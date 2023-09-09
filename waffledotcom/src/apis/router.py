from fastapi.routing import APIRouter

from waffledotcom.src.apis import dummy
from waffledotcom.src.apis import user

api_router = APIRouter()
api_router.include_router(dummy.router)
api_router.include_router(user.router)
