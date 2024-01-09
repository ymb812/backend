import logging
from fastapi import APIRouter, HTTPException, Header, Depends, status
from api.schemas.v1.web_user import WebUserModel, WebUserToBeUpdatedModel
from db.models import WebUser
from configs.settings import env_parameters


# auth header
def authorize_user(X_AUTH_TOKEN: str = Header(None)):
    if X_AUTH_TOKEN != env_parameters.X_AUTH_TOKEN:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True


router = APIRouter(dependencies=[Depends(authorize_user)])
logger = logging.getLogger(__name__)


# create new user
@router.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(body: WebUserModel):
    try:
        await WebUser.create(uuid=body.uuid, email=body.email, password=body.password)
    except Exception as e:
        logger.error(f'Cannot create WebUser via /user with uuid={body.uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='User is not unique or types are wrong')

    return {'uuid': body.uuid, 'status': 'User created successfully.'}


# delete user
@router.delete('/user/{uuid}', status_code=status.HTTP_200_OK)
async def delete_user(uuid: str):
    try:
        await WebUser.filter(uuid=uuid).delete()
    except Exception as e:
        logger.error(f'Cannot delete WebUser with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'User deleted successfully.'}


# update user data
@router.put('/user/{uuid}', status_code=status.HTTP_200_OK)
async def update_user(uuid: str, body: WebUserToBeUpdatedModel):
    try:
        user = await WebUser.get(uuid=uuid)
        await user.update_fields(updated_fields=body)
    except Exception as e:
        logger.error(f'Cannot update WebUser with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='')

    return {'uuid': uuid, 'status': 'User updated successfully.', 'updatedProperties': body.model_dump()}


# get user data
@router.get('/user/{uuid}', status_code=status.HTTP_200_OK)
async def get_user(uuid: str):
    try:
        user = await WebUser.filter(uuid=uuid).first().values()
    except Exception as e:
        logger.error(f'Cannot get WebUser via with uuid={uuid}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Check the uuid')

    return user
