from fastapi.routing import APIRouter

from waffledotcom.src.apps import batch, user

api_router = APIRouter(prefix="/api")
api_router.include_router(user.router)
api_router.include_router(batch.router)
