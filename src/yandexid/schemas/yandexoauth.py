# -*- coding: utf-8 -*-
'''JSON schemas for Yandex ID OAuth API
'''
from pydantic import BaseModel, Field


class Token(BaseModel):
    '''Token response

    Attributes:
        access_token (str): OAuth access token
        token_type (str): Token type. Must be always `bearer`.
        expires_in (int): Token expiration time in seconds
        refresh_token (str): Refresh token
        scope (str | None, optional): Scope of access token. Available only if some scope was declined.
    '''
    access_token: str = Field(..., description='OAuth access token')
    token_type: str = Field(..., description='Token type')
    expires_in: int = Field(..., description='Token expiration time in seconds')
    refresh_token: str = Field(..., description='Refresh token')
    scope: str | None = Field(None, description='Scope of access token')
