from typing import Type, Union, Optional

import pydantic
from flask import jsonify

from app import app


class HttpError(Exception):

    def __init__(self, status_code: int, message: Union[str, dict, list]):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify(
        {
            "status": 'error', 'message': error.message
        }
    )
    response.status_code = error.status_code
    return response


class CreateAdvertSchema(pydantic.BaseModel):
    ad_header: str
    description: str
    owner: str

    @pydantic.validator("ad_header")
    def check_ad_header(cls, value: str):
        if len(value) > 30:
            raise ValueError("Header must be less than 30 chars")
        return value

    @pydantic.validator("description")
    def check_description(cls, value: str):
        if len(value) > 200:
            raise ValueError("Description must be less than 200 chars")
        return value

    @pydantic.validator("owner")
    def check_owner(cls, value: str):
        if len(value) > 30:
            raise ValueError("Description must be less than 30 chars")
        return value


class PatchAdvertSchema(pydantic.BaseModel):
    ad_header: Optional[str]
    description: Optional[str]

    @pydantic.validator("ad_header")
    def check_ad_header(cls, value: str):
        if len(value) > 30:
            raise ValueError("Header must be less than 30 chars")
        return value

    @pydantic.validator("description")
    def check_description(cls, value: str):
        if len(value) > 200:
            raise ValueError("Description must be less than 200 chars")
        return value


def validate(data_to_validate: dict, validation_class: Union[Type[CreateAdvertSchema], Type[PatchAdvertSchema]]):
    try:
        return validation_class(**data_to_validate).dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())
