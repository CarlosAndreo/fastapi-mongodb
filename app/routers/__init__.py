from fastapi import APIRouter

from routers.user import user_router

router = APIRouter(prefix="/api/v1")
router.include_router(router=user_router)
