# -*- coding: utf-8 -*-
'''Yandex ID OAuth API async wrapper

Reference: https://yandex.ru/dev/id/doc/dg/oauth/concepts/about.html
'''
import logging
import warnings
from base64 import b64encode
from urllib.parse import urlencode

from httpx import AsyncClient

from ..__meta import __version__
from ..errors.yandexoauth import (
    InvalidDeviceID, InvalidDeviceName, AuthorizationPending,
    BadVerificationCode, InvalidClient, InvalidGrant, InvalidRequest,
    InvalidScope, UnauthorizedClient, UnsupportedGrantType, YandexOAuthError
)
from ..validators import (
    DeviceID, DeviceName, OptionalScope
)
from ..schemas.yandexoauth import Token


class AsyncYandexOAuth:
    '''Yandex ID OAuth API async wrapper
    '''
    BASE_URL = 'https://oauth.yandex.ru'
    log = logging.getLogger('YandexOAuth')

    def __init__(
        self, client_id: str, client_secret: str, redirect_uri: str,
        scope: str | None = None, client: AsyncClient | None = None
    ):
        '''Initialize YandexOAuth object

        Args:
            client_id (str): Client ID
            client_secret (str): Client secret
            redirect_uri (str): Redirect URI
            scope (str, optional): OAuth Scope. Defaults to None.
            client (httpx.AsyncClient, optional): Client object. Defaults to None.
        '''
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._scope = scope

        self.__headers = {
            'User-Agent': f'YandexID/{__version__}'
        }
        self.__params = {
            'client_id': client_id
        }
        self.__client = client or AsyncClient(
            base_url=self.BASE_URL, params=self.__params,
            headers=self.__headers
        )

    async def _make_request(self, method: str, url: str, **kwargs) -> dict:
        '''Make request to Yandex OAuth API

        Args:
            method (str): HTTP method
            url (str): URL to request

        Returns:
            dict: Response data
        '''
        response = await self.__client.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_authorization_url(
        self, response_type: str = 'code', device_id: str | None = None,
        device_name: str | None = None, login_hint: str | None = None,
        scope: str | None = None, optional_scope: str | None = None,
        force_confirm: bool | None = None, state: str | None = None
    ) -> str:
        '''Get authorization URL.
        Reference: https://yandex.ru/dev/id/doc/dg/oauth/reference/auto-code-client.html#auto-code-client__get-code

        Args:
            response_type (str, optional): Response type. Defaults to 'code'.
            device_id (str, optional): Device ID. Defaults to None.
            device_name (str, optional): Device name. Defaults to None.
            login_hint (str, optional): Login hint. Defaults to None.
            scope (str, optional): OAuth scope. Defaults to None.
            optional_scope (str, optional): Optional OAuth scope. Defaults to None.
            force_confirm (bool, optional): Force confirm. Defaults to None.
            state (str, optional): State. Defaults to None.

        Note:
            Check available `optional_scope` for your app here: https://oauth.yandex.ru/client/<client_id>/info.
            `response_type` can be 'code' or 'token'.

        Raises:
            InvalidDeviceID: If device_id is invalid.
            InvalidDeviceName: If device_name is invalid.

        Returns:
            str: Authorization URL
        '''
        params = {
            'response_type': response_type,
            'redirect_uri': self._redirect_uri,
            'client_id': self._client_id
        }
        if device_id:
            try:
                DeviceID.validate(device_id)
            except InvalidDeviceID as e:
                self.log.error(e)
                raise e
            else:
                params['device_id'] = device_id
                if not device_name:
                    warnings.warn(
                        'device_id is specified, but device_name is not. '
                        'Yandex ID returns token for unknown device.', UserWarning
                    )
        if device_name:
            try:
                DeviceName.validate(device_name)
            except InvalidDeviceName as e:
                self.log.error(e)
                raise e
            else:
                params['device_name'] = device_name
                if not device_id:
                    warnings.warn(
                        'device_name is specified, but device_id is not. '
                        'device_name will be ignored.', UserWarning
                    )
        if login_hint:
            params['login_hint'] = login_hint
        if scope:
            params['scope'] = scope
        if optional_scope:
            if self._scope or scope:
                if self._scope:
                    test_scope = self._scope
                elif scope:
                    test_scope = scope
                else:
                    test_scope = None
                if test_scope:
                    OptionalScope.validate(test_scope, optional_scope)
            params['optional_scope'] = optional_scope
        if force_confirm:
            params['force_confirm'] = str(int(force_confirm))
        if state:
            params['state'] = state
        return f'{self.BASE_URL}/authorize?{urlencode(params)}'

    async def get_token_from_code(
        self, code: str, device_id: str | None = None,
        device_name: str | None = None
    ) -> Token:
        '''Get token from code
        Reference: https://yandex.ru/dev/id/doc/dg/oauth/reference/auto-code-client.html#auto-code-client__get-token

        Args:
            code (str): Verification code.
            device_id (str, optional): Device ID. Defaults to None.
            device_name (str, optional): Device name. Defaults to None.

        Raises:
            InvalidDeviceID: If device_id is invalid.
            InvalidDeviceName: If device_name is invalid.
            YandexOAuthError: If Yandex OAuth API returns error.

        Returns:
            Token: Token object
        '''
        url = '/token'
        method = 'POST'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
        }
        if device_id:
            try:
                DeviceID.validate(device_id)
            except InvalidDeviceID as e:
                self.log.error(e)
                raise e
            else:
                data['device_id'] = device_id
                if not device_name:
                    warnings.warn(
                        'device_id is specified, but device_name is not. '
                        'Yandex ID returns token for unknown device.', UserWarning
                    )
        if device_name:
            try:
                DeviceName.validate(device_name)
            except InvalidDeviceName as e:
                self.log.error(e)
                raise e
            else:
                data['device_name'] = device_name
                if not device_id:
                    warnings.warn(
                        'device_name is specified, but device_id is not. '
                        'device_name will be ignored.', UserWarning
                    )
        headers = {
            'Authorization': f'Basic {b64encode(f"{self._client_id}:{self._client_secret}".encode()).decode()}'
        }
        response = await self._make_request(method, url, data=data, headers=headers)
        if 'error' in response:
            match response['error']:
                case 'authorization_pending':
                    raise AuthorizationPending(response['error_description'])
                case 'bad_verification_code':
                    raise BadVerificationCode(response['error_description'])
                case 'invalid_client':
                    raise InvalidClient(response['error_description'])
                case 'invalid_grant':
                    raise InvalidGrant(response['error_description'])
                case 'invalid_request':
                    raise InvalidRequest(response['error_description'])
                case 'invalid_scope':
                    raise InvalidScope(response['error_description'])
                case 'unauthorized_client':
                    raise UnauthorizedClient(response['error_description'])
                case 'unsupported_grant_type':
                    raise UnsupportedGrantType(response['error_description'])
                case _:
                    raise YandexOAuthError(response['error_description'])
        return Token(**response)

    async def get_token_from_refresh_token(self, refresh_token: str) -> Token:
        '''Get token from refresh token
        Reference: https://yandex.ru/dev/id/doc/dg/oauth/reference/refresh-client.html#refresh-client__get-token

        Args:
            refresh_token (str): Refresh token.

        Raises:
            YandexOAuthError: If Yandex OAuth API returns error.

        Returns:
            Token: Token object
        '''
        url = '/token'
        method = 'POST'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        headers = {
            'Authorization': f'Basic {b64encode(f"{self._client_id}:{self._client_secret}".encode()).decode()}'
        }
        response = await self._make_request(method, url, data=data, headers=headers)
        if 'error' in response:
            match response['error']:
                case 'invalid_client':
                    raise InvalidClient(response['error_description'])
                case 'invalid_grant':
                    raise InvalidGrant(response['error_description'])
                case 'invalid_request':
                    raise InvalidRequest(response['error_description'])
                case 'unauthorized_client':
                    raise UnauthorizedClient(response['error_description'])
                case 'unsupported_grant_type':
                    raise UnsupportedGrantType(response['error_description'])
                case _:
                    raise YandexOAuthError(response['error_description'])
        return Token(**response)

    async def revoke_token(self, access_token: str) -> bool:
        '''Revoke token
        Reference: https://yandex.ru/dev/id/doc/dg/oauth/concepts/device-token.html#device-token-revoke__cleartext

        Args:
            access_token (str): OAuth access token.

        Raises:
            YandexOAuthError: If Yandex OAuth API returns error.

        Returns:
            bool: True if token was revoked successfully, False otherwise.
        '''
        url = '/revoke_token'
        method = 'POST'
        data = {
            'access_token': access_token
        }
        headers = {
            'Authorization': f'Basic {b64encode(f"{self._client_id}:{self._client_secret}".encode()).decode()}'
        }
        response = await self._make_request(method, url, data=data, headers=headers)
        if 'error' in response:
            match response['error']:
                case 'invalid_client':
                    raise InvalidClient(response['error_description'])
                case 'invalid_request':
                    raise InvalidRequest(response['error_description'])
                case 'unauthorized_client':
                    raise UnauthorizedClient(response['error_description'])
                case _:
                    raise YandexOAuthError(response['error_description'])
        return True
