import logging
from fastapi import APIRouter, HTTPException, Header, Depends, status
from core.webhooks.models import ProductModel, ProductToBeUpdatedModel
from core.db.models import Product
from configs.settings import env_parameters


# auth header
def authorize_user(auth_token: str = Header(None)):
    if auth_token != env_parameters.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True


router = APIRouter(dependencies=[Depends(authorize_user)])
logger = logging.getLogger(__name__)


# create new product
@router.post('/product', status_code=status.HTTP_201_CREATED)
async def create_product(body: ProductModel):
    try:
        await Product.create(uuid=body.uuid, web_shop_id=body.web_shop_uuid, article=body.article, name=body.name,
                             description=body.description, discount_percent=body.discount_percent,
                             category_id=body.category_uuid, media_data=body.media_data,
                             order_priority=body.order_priority)
    except Exception as e:
        logger.error(f'Cannot create Product via /product with uuid={body.uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Product is not unique or types are wrong')

    return {'uuid': body.uuid, 'status': 'Product created successfully.'}


# delete product
@router.delete('/product/{uuid}', status_code=status.HTTP_200_OK)
async def delete_product(uuid: str):
    try:
        await Product.filter(uuid=uuid).delete()
    except Exception as e:
        logger.error(f'Cannot delete Product via /product with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Product deleted successfully.'}


# update product data
@router.put('/product/{uuid}', status_code=status.HTTP_200_OK)
async def update_product(uuid: str, body: ProductToBeUpdatedModel):
    try:
        product = await Product.get(uuid=uuid)
        await product.update_fields(updated_fields=body)
    except Exception as e:
        logger.error(f'Cannot update Product with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Product updated successfully.', 'updatedProperties': body.model_dump()}


# get product data
@router.get('/product/{uuid}', status_code=status.HTTP_200_OK)
async def get_product(uuid: str):
    try:
        product = await Product.filter(uuid=uuid).first().values()
    except Exception as e:
        logger.error(f'Cannot get Product with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Check the uuid')

    return product
