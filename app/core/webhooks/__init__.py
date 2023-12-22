from fastapi import FastAPI
from core.webhooks import user_handlers, shop_handlers, product_handlers


app = FastAPI()
app.include_router(user_handlers.router)
app.include_router(shop_handlers.router)
app.include_router(product_handlers.router)

