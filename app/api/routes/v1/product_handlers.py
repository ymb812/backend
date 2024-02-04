import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Header, Depends, status
from api.schemas.v1.product import ProductModel, ProductToBeUpdatedModel, ProductFromDBModel, ProductsByShopModel
from db.models import Product
from configs.settings import env_parameters


# auth header
def authorize_user(X_AUTH_TOKEN: str = Header(None)):
    if X_AUTH_TOKEN != env_parameters.X_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True


router = APIRouter(dependencies=[Depends(authorize_user)])
logger = logging.getLogger(__name__)


# create new product
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductModel.Response)
async def create_product(user_uuid: str, body: ProductModel.Request):
    try:
        product_uuid = uuid4()
        await Product.create(uuid=product_uuid, web_shop_id=body.web_shop_uuid, article=body.article, name=body.name,
                             description=body.description, discount_percent=body.discount_percent,
                             category_id=body.category_uuid, media_data=body.media_data,
                             order_priority=body.order_priority)
    except Exception as e:
        logger.error(f'Cannot create Product via /product', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Product is not unique or types are wrong')

    return {'uuid': product_uuid, 'status': 'Product created successfully.'}


# delete product
@router.delete('/{uuid}', status_code=status.HTTP_200_OK, response_model=ProductModel.Response)
async def delete_product(uuid: str, user_uuid: str):
    try:
        if not await Product.filter(uuid=uuid).delete():
            return {'uuid': uuid, 'status': 'Product does not exist.'}
    except Exception as e:
        logger.error(f'Cannot delete Product via /product with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Product deleted successfully.'}


# update product data
@router.patch('/{uuid}', status_code=status.HTTP_200_OK, response_model=ProductToBeUpdatedModel.Response,
              responses={200: {'description': 'Successful Response. '
                                              'If field in updatedProperties is None, then it may not be updated'}})
async def update_product(uuid: str, user_uuid: str, body: ProductToBeUpdatedModel.Request):
    try:
        product = await Product.get(uuid=uuid)
        await product.update_fields(updated_fields=body)
    except Exception as e:
        logger.error(f'Cannot update Product with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Product updated successfully.', 'updatedProperties': body.model_dump()}


# get product data
@router.get('/{uuid}', status_code=status.HTTP_200_OK, response_model=ProductFromDBModel.Response,
            responses={404: {'description': 'Product does not exist'}})
async def get_product(uuid: str, user_uuid: str):
    try:
        product = await Product.filter(uuid=uuid).first().values()
    except Exception as e:
        logger.error(f'Cannot get Product with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Check the uuid')

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product does not exist')

    return product


# get all products by shop
@router.get('/all_products_by_shop/{shop_uuid}', status_code=status.HTTP_200_OK,
            response_model=ProductsByShopModel.Response)
async def get_products_by_shop(shop_uuid: str, user_uuid: str, offset: int = 0, limit: int | None = None):
    try:
        if limit is not None:
            products = await Product.filter(
                web_shop_id=shop_uuid).offset(offset).limit(limit).all().values()
        else:
            products = await Product.filter(web_shop_id=shop_uuid).offset(offset).all().values()

    except Exception as e:
        logger.error(f'Cannot get Products by shop_uuid={shop_uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Check the uuid')

    return {'amount': len(products), 'products': products}
