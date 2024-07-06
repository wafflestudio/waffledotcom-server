from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1/health", tags=["batch"])


@v1_router.get("/")
def health_check():
    # 현재로서는 추가로 체크할 게 없으므로 서버만 살아있는지 확인
    return {"status": "OK"}
