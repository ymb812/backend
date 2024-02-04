import datetime
from pydantic import BaseModel, EmailStr, UUID4


# post request
class WebUserModel:
    class Request(BaseModel):
        uuid: str
        email: EmailStr

    class Response(BaseModel):
        uuid: str
        status: str


class WebUserToBeUpdatedInfoModel(BaseModel):
    email: EmailStr | None = None


# user put request
class WebUserToBeUpdatedModel:
    class Request(WebUserToBeUpdatedInfoModel):
        pass

    class Response(WebUserModel.Response):
        updatedProperties: WebUserToBeUpdatedInfoModel


# get request
class WebUserFromDBModel:
    class Response(BaseModel):
        uuid: UUID4
        email: EmailStr
        created_at: datetime.datetime
        updated_at: datetime.datetime
