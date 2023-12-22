import logging
from fastapi import APIRouter, HTTPException, Header, Depends, status
from core.webhooks.models import WebShopModel, WebShopToBeUpdatedModel, WebShopStaticContentModel
from core.db.models import WebShop
from configs.settings import env_parameters


# auth header
def authorize_user(auth_token: str = Header(None)):
    if auth_token != env_parameters.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True


router = APIRouter(dependencies=[Depends(authorize_user)])
logger = logging.getLogger(__name__)


# create new user
@router.post('/shop', status_code=status.HTTP_201_CREATED)
async def create_shop(body: WebShopModel):
    try:
        await WebShop.create(uuid=body.uuid, name=body.name, bot_id=body.bot_id)

        # here get bot_token from bot_manager
        bot_token = 'will_be_received_from_bot_manager'

    except Exception as e:
        logger.error(f'Cannot create WebShop via /shop with uuid={body.uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Shop is not unique or types are wrong')

    return {'uuid': body.uuid, 'bot_token': bot_token, 'status': 'Shop created successfully.'}


# delete shop
@router.delete('/shop/{uuid}', status_code=status.HTTP_200_OK)
async def delete_shop(uuid: str):
    try:
        await WebShop.filter(uuid=uuid).delete()
    except Exception as e:
        logger.error(f'Cannot delete WebShop with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Shop deleted successfully.'}


# update shop data
@router.put('/shop/{uuid}', status_code=status.HTTP_200_OK)
async def update_shop(uuid: str, body: WebShopToBeUpdatedModel):
    try:
        updated_data = await WebShop.update_data_from_api(uuid=uuid, name=body.name, bot_id=body.bot_id)
    except Exception as e:
        logger.error(f'Cannot update WebShop with uuid={body.uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Shop updated successfully.', 'updatedProperties': updated_data}


# get shop data
@router.get('/shop/{uuid}', status_code=status.HTTP_200_OK)
async def get_shop(uuid: str):
    try:
        shop = await WebShop.filter(uuid=uuid).first().values()
    except Exception as e:
        logger.error(f'Cannot get WebShop with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Check the uuid')

    return shop


# update shop static content
@router.put('/shop/static', status_code=status.HTTP_200_OK)
async def update_shop_static_content(uuid: str, body: WebShopStaticContentModel):
    pass
