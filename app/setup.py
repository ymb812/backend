from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from api import router
from db import get_config as get_db_config, get_connection

app = FastAPI(title='TS-ShopBackend', debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.include_router(router)
register_tortoise(app=app, config=get_db_config(get_connection()), generate_schemas=True)
