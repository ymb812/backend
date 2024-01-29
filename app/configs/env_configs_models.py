from pydantic import BaseModel


class APPSettings(BaseModel):
    DEBUG: bool


class APIConfigsModel(BaseModel):
    X_AUTH_TOKEN: str
    ITEMS_PER_PAGE: int


class DataBaseConfigsModel(BaseModel):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str


class RestAPISettings(BaseModel):
    REST_HOST: str
    REST_PORT: int


class EnvConfigsModel(APPSettings, APIConfigsModel, DataBaseConfigsModel, RestAPISettings):
    pass
