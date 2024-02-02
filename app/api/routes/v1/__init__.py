from fastapi import APIRouter
from api.routes.v1 import user_handlers, product_handlers, shop_handlers

router = APIRouter()
router.include_router(user_handlers.router, prefix='/user', tags=['v1/user'])
router.include_router(shop_handlers.router, prefix='/shop', tags=['v1/shop'])
router.include_router(product_handlers.router, prefix='/product', tags=['v1/product'])
