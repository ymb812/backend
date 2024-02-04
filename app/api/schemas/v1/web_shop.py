import datetime
from pydantic import BaseModel, UUID4


# post request
class WebShopModel:
    class Request(BaseModel):
        name: str
        bot_id: int

    class Response(BaseModel):
        uuid: UUID4
        status: str


class WebShopToBeUpdatedInfoModel(BaseModel):
    name: str | None = None
    bot_id: int | None = None


# patch request
class WebShopToBeUpdatedModel:
    class Request(WebShopToBeUpdatedInfoModel):
        pass

    class Response(WebShopModel.Response):
        updatedProperties: WebShopToBeUpdatedInfoModel


# get request
class WebShopFromDBModel:
    class Response(BaseModel):
        uuid: UUID4
        name: str
        bot_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime


# update shop static content
class WebShopStaticContentModel:
    # to be added
    class Request(BaseModel):
        uuid: UUID4

    class Response(BaseModel):
        pass
