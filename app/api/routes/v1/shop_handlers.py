import logging
import aiohttp
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


# create new shop
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=WebShopModel.Response,
             responses={503: {'description': 'Error in IDP API response'},
                        500: {'description': 'bot_id is not unique'}})
async def create_shop(user_uuid: str, body: WebShopModel.Request):
    # get bot_username from bot manager
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{env_parameters.IDP_BOT_USERNAME_ROUTE}/{body.bot_id}') as response:
                response = await response.json(content_type='text')
                bot_username = response['username']
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=f'Error with IDP API response: {response}')

    try:
        webshop_uuid = uuid4()
        await WebShop.create(uuid=webshop_uuid, name=body.name, bot_id=body.bot_id, bot_username=bot_username)
    except Exception as e:
        logger.error(f'Cannot create WebShop via /shop', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Bot_id is not unique')

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

    return {'status': 'Shop updated successfully.', 'data': shop}


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
