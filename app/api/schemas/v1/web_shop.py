from pydantic import BaseModel


# shop model
class WebShopModel(BaseModel):
    uuid: str
    name: str
    bot_id: int


# shop put request
class WebShopToBeUpdatedModel(BaseModel):
    name: str | None
    bot_id: int | None


# update shop static content
class WebShopStaticContentModel(BaseModel):
    uuid: str
    # to be added
