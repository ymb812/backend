from pydantic import BaseModel, EmailStr


# main user model
class WebUserModel(BaseModel):
    uuid: str
    email: EmailStr


# user put request
class WebUserToBeUpdatedModel(BaseModel):
    email: EmailStr | None
