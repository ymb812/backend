from fastapi import APIRouter
from api.routes.v1 import user_handlers, product_handlers, shop_handlers

router = APIRouter()
router.include_router(user_handlers.router)
router.include_router(shop_handlers.router)
router.include_router(product_handlers.router)
