import logging
from fastapi import APIRouter, HTTPException, Header, Depends, status
from api.schemas.v1.web_shop import WebShopModel, WebShopToBeUpdatedModel, WebShopStaticContentModel
from db.models import WebShop
from configs.settings import env_parameters


# auth header
def authorize_user(X_AUTH_TOKEN: str = Header(None)):
    if X_AUTH_TOKEN != env_parameters.X_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True


router = APIRouter(dependencies=[Depends(authorize_user)])
logger = logging.getLogger(__name__)


# create new user
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_shop(user_uuid: str, body: WebShopModel):
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
@router.delete('/{uuid}', status_code=status.HTTP_200_OK)
async def delete_shop(user_uuid: str, uuid: str):
    try:
        await WebShop.filter(uuid=uuid).delete()
    except Exception as e:
        logger.error(f'Cannot delete WebShop with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Shop deleted successfully.'}


# update shop data
@router.patch('/{uuid}', status_code=status.HTTP_200_OK)
async def update_shop(user_uuid: str, uuid: str, body: WebShopToBeUpdatedModel):
    try:
        shop = await WebShop.get(uuid=uuid)
        await shop.update_fields(updated_fields=body)
    except Exception as e:
        logger.error(f'Cannot update WebShop with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Shop updated successfully.', 'updatedProperties': body.model_dump()}


# get shop data
@router.get('/{uuid}', status_code=status.HTTP_200_OK)
async def get_shop(user_uuid: str, uuid: str):
    try:
        shop = await WebShop.filter(uuid=uuid).first().values()
    except Exception as e:
        logger.error(f'Cannot get WebShop with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Check the uuid')

    return shop


# update shop static content
@router.put('/static', status_code=status.HTTP_200_OK)
async def update_shop_static_content(user_uuid: str, uuid: str, body: WebShopStaticContentModel):
    pass
