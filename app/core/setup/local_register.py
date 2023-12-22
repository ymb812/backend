from fastapi import FastAPI
from core import db


def register_something(app: FastAPI, **kwargs):
    @app.on_event('startup')
    async def start_local_bot():
        await db.init()

    @app.on_event('shutdown')
    async def stop_local_bot():
        await db.close()
