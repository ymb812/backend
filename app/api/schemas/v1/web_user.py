import datetime
from pydantic import BaseModel, EmailStr, UUID4


# post request
class WebUserModel:
    class Request(BaseModel):
        email: EmailStr

    class Response(BaseModel):
        uuid: UUID4
        status: str


class WebUserToBeUpdatedInfoModel(BaseModel):
    email: EmailStr | None = None


# get request
class WebUserFromDBModel:
    class Response(BaseModel):
        uuid: UUID4
        email: EmailStr
        created_at: datetime.datetime
        updated_at: datetime.datetime


# user put request
class WebUserToBeUpdatedModel:
    class Request(WebUserToBeUpdatedInfoModel):
        pass

    class Response(BaseModel):
        status: str
        data: WebUserFromDBModel.Response
