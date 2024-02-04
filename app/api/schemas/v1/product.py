import datetime
from pydantic import BaseModel, UUID4
from typing import List


# post request
class ProductModel:
    class Request(BaseModel):
        web_shop_uuid: UUID4
        article: str | None = None
        name: str | None = None
        description: str
        discount_percent: float | None = None
        category_uuid: UUID4
        media_data: str | None = None
        order_priority: int | None = None

    class Response(BaseModel):
        uuid: UUID4
        status: str


class ProductToBeUpdatedInfoModel(BaseModel):
    article: str | None = None
    name: str | None = None
    description: str | None = None
    discount_percent: float | None = None
    category_uuid: UUID4 | None = None
    media_data: str | None = None
    order_priority: int | None = None


# patch request
class ProductToBeUpdatedModel:
    class Request(ProductToBeUpdatedInfoModel):
        pass

    class Response(ProductModel.Response):
        updatedProperties: ProductToBeUpdatedInfoModel


# get request
class ProductFromDBModel:
    class Response(BaseModel):
        uuid: UUID4
        web_shop_id: UUID4
        article: str | None
        name: str | None
        description: str
        discount_percent: float
        category_id: UUID4
        media_data: str | None
        order_priority: int
        created_at: datetime.datetime
        updated_at: datetime.datetime


class ProductsByShopModel:
    class Response(BaseModel):
        amount: int
        products: List[ProductFromDBModel.Response]
