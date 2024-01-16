from pydantic import BaseModel


# post request
class ProductModel(BaseModel):
    uuid: str
    web_shop_uuid: str
    article: str | None
    name: str | None
    description: str
    discount_percent: float | None
    category_uuid: str
    media_data: str | None
    order_priority: int | None


# put request
class ProductToBeUpdatedModel(BaseModel):
    article: str | None
    name: str | None
    description: str | None
    discount_percent: float | None
    category_uuid: str | None
    media_data: str | None
    order_priority: int | None
