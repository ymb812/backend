import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Header, Depends, status
from api.schemas.v1.web_shop import WebShopModel, WebShopToBeUpdatedModel, WebShopStaticContentModel, WebShopFromDBModel
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
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=WebShopModel.Response)
async def create_shop(user_uuid: str, body: WebShopModel.Request):
    try:
        webshop_uuid = uuid4()
        await WebShop.create(uuid=webshop_uuid, name=body.name, bot_id=body.bot_id)

        # here get bot_token from bot_manager
        bot_token = 'will_be_received_from_bot_manager'

    except Exception as e:
        logger.error(f'Cannot create WebShop via /shop', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Shop is not unique or types are wrong')

    return {'uuid': webshop_uuid, 'status': 'Shop created successfully.'}


# delete shop
@router.delete('/{uuid}', status_code=status.HTTP_200_OK, response_model=WebShopModel.Response)
async def delete_shop(user_uuid: str, uuid: str):
    try:
        await WebShop.filter(uuid=uuid).delete()
    except Exception as e:
        logger.error(f'Cannot delete WebShop with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Shop deleted successfully.'}


# update shop data
@router.patch('/{uuid}', status_code=status.HTTP_200_OK, response_model=WebShopToBeUpdatedModel.Response,
              responses={200: {'description': 'Successful Response. '
                                              'If field in updatedProperties is None, then it may not be updated'}})
async def update_shop(user_uuid: str, uuid: str, body: WebShopToBeUpdatedModel.Request):
    try:
        shop = await WebShop.get(uuid=uuid)
        await shop.update_fields(updated_fields=body)
    except Exception as e:
        logger.error(f'Cannot update WebShop with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'Shop updated successfully.', 'updatedProperties': body.model_dump()}


# get shop data
@router.get('/{uuid}', status_code=status.HTTP_200_OK, response_model=WebShopFromDBModel.Response,
            responses={404: {'description': 'Shop does not exist'}})
async def get_shop(user_uuid: str, uuid: str):
    try:
        shop = await WebShop.filter(uuid=uuid).first().values()
    except Exception as e:
        logger.error(f'Cannot get WebShop with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Check the uuid')

    if shop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shop does not exist')

    return shop


# update shop static content
@router.put('/static', status_code=status.HTTP_200_OK, response_model=WebShopStaticContentModel.Response)
async def update_shop_static_content(user_uuid: str, uuid: str, body: WebShopStaticContentModel.Request):
    pass
