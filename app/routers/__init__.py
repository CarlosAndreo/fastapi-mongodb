from fastapi import APIRouter

from routers.auth import auth_router
from routers.me import me_router

router = APIRouter(prefix="/api/v1")
router.include_router(router=auth_router)
router.include_router(router=me_router)
