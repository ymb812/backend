from pydantic import BaseModel


# main user model
class WebUserModel(BaseModel):
    uuid: str
    email: str
    password: str


# user put request
class WebUserToBeUpdatedModel(BaseModel):
    email: str | None
    password: str | None


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


# product model
class ProductModel(BaseModel):
    uuid: str
    web_shop_uuid: str
    article: str | None
    name: str | None
    description: str
    discount_percent: float = 0
    category_uuid: str
    media_data: str | None
    order_priority: int = 0


# product put request - how to do it better?
class ProductToBeUpdatedModel(BaseModel):
    article: str | None
    name: str | None
    description: str | None
    discount_percent: float | None
    category_uuid: str | None
    media_data: str | None
    order_priority: int | None
