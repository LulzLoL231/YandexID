# -*- coding: utf-8 -*-
'''JSON schemas for Yandex ID API

Reference: https://yandex.ru/dev/id/doc/dg/api-id/reference/response.html
'''
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, validator

from avatar_utils import get_avatar_url


class Sex(str, Enum):
    '''User sex enum

    Attributes:
        MALE (str): Sex is male
        WOMAN (str): Sex is woman
    '''
    MALE = 'male'
    WOMAN = 'woman'


class Phone(BaseModel):
    '''User phone

    Attributes:
        id (int): Phone ID in Yandex
        number (str): Phone number in Yandex
    '''
    id: int = Field(..., description='Phone ID in Yandex')
    number: str = Field(..., description='Phone number in Yandex')


class User(BaseModel):
    '''User info

    Attributes:
        login (str): User login in Yandex
        id (str): User ID in Yandex
        client_id (str): Client ID by oauth token
        psuid (str): User ID bassed on client_id and client_secret by Yandex
        openid_identities (list[str], optional): Yandex OpenID identities
        default_email (str, optional): Default email of user in Yandex
        email (list[str], optional): List of emails of user in Yandex
        default_avatar_id (str, optional): Default avatar ID of user in Yandex
        is_avatar_empty (bool, optional): Flag of default avatar of user in Yandex
        birthday (datetime | str | None): Birthday of user in Yandex
        first_name (str, optional): First name of user in Yandex
        last_name (str, optional): Last name of user in Yandex
        display_name (str, optional): Display name of user in Yandex
        real_name (str, optional): Real name of user in Yandex
        sex (schemas.Sex, optional): User sex in Yandex
        default_phone (schemas.Phone, optional): Default phone of user in Yandex.

    Note:
        `openid_identities` field is available only with `with_openid_identity` param
        `default_email` and `emails` fields are available only with `login:email` scope
        `default_avatar_id` and `is_avatar_empty` fields are available only with `login:avatar` scope
        `birthday` field is available only with `login:birthday` scope
        `first_name`, `last_name`, `display_name`, `real_name` and `sex` fields are available only with `login:info` scope
        `default_phone` field is available only with `login:phone` scope
        `birthday` field can be str, because Yandex API can return it with zeros in string.

    Reference:
        https://yandex.ru/dev/id/doc/dg/api-id/reference/response.html
    '''
    login: str = Field(..., description='User login in Yandex')
    id: str = Field(..., description='User ID in Yandex')
    client_id: str = Field(..., description='Client ID by oauth token')
    psuid: str = Field(
        ..., description='User ID bassed on client_id and client_secret by Yandex'
    )

    # Only with `with_openid_identity` param
    openid_identities: list[str] | None = Field(
        None, description='Yandex OpenID identities'
    )

    # Only with `login:email` scope
    default_email: str | None = Field(
        None, description='Default email of user in Yandex'
    )
    emails: list[str] | None = Field(
        None, description='List of emails of user in Yandex'
    )

    # Only with `login:avatar` scope
    default_avatar_id: str | None = Field(
        None, description='Default avatar ID of user in Yandex'
    )
    is_avatar_empty: bool | None = Field(
        None, description='Flag of default avatar of user in Yandex'
    )

    # Only with `login:birthday` scope
    birthday: datetime | str | None = Field(
        None, description='Birthday of user in Yandex'
    )

    # Only with `login:info` scope
    first_name: str | None = Field(
        None, description='First name of user in Yandex'
    )
    last_name: str | None = Field(
        None, description='Last name of user in Yandex'
    )
    display_name: str | None = Field(
        None, description='Display name of user in Yandex'
    )
    real_name: str | None = Field(
        None, description='First and last name of user in Yandex'
    )
    sex: Sex | None = Field(
        None, description='Sex of user in Yandex'
    )

    # Only with `login:default_phone` scope
    default_phone: Phone | None = Field(
        None, description='Default phone of user in Yandex'
    )

    @validator('birthday', pre=True)
    def parse_birthday(cls, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d')
        except Exception:
            return value

    def get_avatar_url(self, size: str = 'islands-200') -> str | None:
        '''Get avatar url by size

    Args:
        avatar_id (str): Avatar ID.
        size (str, optional): Avatar size. Default is `islands-200`.

    Note:
        size can be:\n
            - `islands-small` - 28x28;\n
            - `islands-34` - 34x34;\n
            - `islands-middle` - 42x42;\n
            - `islands-50` - 50x50;\n
            - `islands-retina-small` - 56x56;\n
            - `islands-68` - 68x68;\n
            - `islands-75` - 75x75;\n
            - `islands-retina-middle` - 84x84;\n
            - `islands-retina-50` - 100x100;\n
            - `islands-200` - 200x200;\n

    Returns:
        str | None: Avatar url
        '''
        if self.default_avatar_id is None:
            return None

        return get_avatar_url(self.default_avatar_id, size)
