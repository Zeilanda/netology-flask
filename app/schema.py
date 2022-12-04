import re
from typing import Optional, Type, Dict, Any

from errors import ApiError
from config import PASSWORD_LENGTH
from pydantic import BaseModel, EmailStr, validator, ValidationError

PASSWORD_REGEX = re.compile(
    "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])*.{{{password_length},}}$".format(
        password_length=PASSWORD_LENGTH
    )
)


class Register(BaseModel):

    email: EmailStr
    password: str

    @validator("password")
    def strong_password(cls, value: str):
        if not PASSWORD_REGEX.match(value):
            raise ValueError("password is too easy")
        return value


class Login(BaseModel):

    email: EmailStr
    password: str


class PatchUser(BaseModel):

    email: Optional[EmailStr]
    password: Optional[str]


SCHEMA_TYPE = Type[Register] | Type[Login] | Type[PatchUser]


def validate(schema: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True) -> dict:
    try:
        validated = schema(**data).dict(exclude_none=exclude_none)
    except ValidationError as er:
        raise ApiError(400, er.errors())
    return validated
