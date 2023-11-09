from fastapi.routing import APIRouter

from waffledotcom.src.apps import user

api_router = APIRouter(prefix="/api")
api_router.include_router(user.router)
