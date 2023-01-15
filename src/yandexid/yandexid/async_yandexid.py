# -*- coding: utf-8 -*-
'''Yandex ID API async wrapper
'''
import logging
from warnings import warn

from httpx import AsyncClient

from ..schemas.yandexid import User
from ..__meta import __version__


class AsyncYandexID:
    '''Yandex ID API async wrapper
    '''
    BASE_URL = 'https://login.yandex.ru'
    log = logging.getLogger('YandexID')

    def __init__(self, oauth_token: str, client: AsyncClient | None = None):
        '''Initialize YandexID object

        Args:
            oauth_token (str): OAuth access token.
            client (httpx.AsyncClient, optional): Client object. Defaults to None.
        '''
        self._oauth_token = oauth_token

        self.__headers = {
            'User-Agent': f'YandexID/{__version__}',
            'Authorization': f'OAuth {oauth_token}'
        }
        self.__client = client or AsyncClient(
            headers=self.__headers, base_url=self.BASE_URL)

    async def _make_request(self, url: str, **kwargs) -> dict:
        '''Make request to Yandex ID API

        Args:
            url (str): URL to request

        Returns:
            dict: Response data
        '''
        response = await self.__client.request('GET', url, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get_user_info(
        self, format: str = 'json', jwt_secret: str | None = None,
        with_openid_identity: bool = False
    ) -> dict:
        '''Get user info

        Args:
            format (str, optional): Response format. Defaults to 'json'.
            jwt_secret (str, optional): JWT secret. Defaults to None.
            with_openid_identity (bool, optional): Include OpenID identity. Defaults to False.

        Note:
            Yandex recommends to not use `jwt_secret` for security reasons.

        Returns:
            dict: Response data
        '''
        url = '/info'
        if jwt_secret is not None:
            warn('Using jwt_secret is not recommended for security reasons', stacklevel=2)
        params = {
            'format': format,
            'with_openid_identity': int(with_openid_identity),
            'jwt_secret': jwt_secret
        }
        return await self._make_request(url, params=params)

    async def get_user_info_json(self, with_openid_identity: bool = False) -> User:
        '''Get user info in JSON format

        Args:
            with_openid_identity (bool, optional): Include OpenID identity. Defaults to False.

        Returns:
            User: User info
        '''
        data = await self.get_user_info(
            format='json', with_openid_identity=with_openid_identity)
        return User(**data)

    async def get_user_info_xml(self, with_openid_identity: bool = False) -> str:
        '''Get user info in XML format

        Args:
            with_openid_identity (bool, optional): Include OpenID identity. Defaults to False.

        Note:
            XML validation is not implemented.

        Returns:
            str: User info
        '''
        data = await self.get_user_info(
            format='xml', with_openid_identity=with_openid_identity)
        return str(data)

    async def get_user_info_jwt(
        self, jwt_secret: str | None = None, with_openid_identity: bool = False
    ) -> str:
        '''Get user info in JWT format

        Args:
            jwt_secret (str, optional): JWT secret. Defaults to None.
            with_openid_identity (bool, optional): Include OpenID identity. Defaults to False.

        Note:
            JWT validation is not implemented.

        Returns:
            str: User info
        '''
        data = await self.get_user_info(
            format='jwt', jwt_secret=jwt_secret,
            with_openid_identity=with_openid_identity
        )
        return str(data)
