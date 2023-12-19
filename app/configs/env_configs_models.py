from typing import Union
from pydantic import BaseModel


class TelegramConfigsModel(BaseModel):
    TELEGRAM_BOT_TOKEN: Union[str]


class DataBaseConfigsModel(BaseModel):
    DB_USERNAME: Union[str]
    DB_PASSWORD: Union[str]
    DB_HOST: Union[str]
    DB_PORT: Union[int]
    DB_NAME: Union[str]


class EnvConfigsModel(TelegramConfigsModel, DataBaseConfigsModel):
    pass
