# -*- coding: utf-8 -*-
'''Yandex ID OAuth API exceptions
'''


class YandexOAuthError(Exception):
    '''Base Yandex OAuth exception
    '''
    pass


class InvalidDeviceID(YandexOAuthError):
    '''Invalid device ID exception
    '''
    pass


class InvalidDeviceName(YandexOAuthError):
    '''Invalid device name exception
    '''
    pass


class AuthorizationPending(YandexOAuthError):
    '''User is not authorized yet
    '''
    pass


class BadVerificationCode(YandexOAuthError):
    '''Verification code from request is not 7 digits.
    '''
    pass


class InvalidClient(YandexOAuthError):
    '''Client ID or client secret is invalid
    '''
    pass


class InvalidGrant(YandexOAuthError):
    '''Invalid or expired verification code
    '''
    pass


class InvalidRequest(YandexOAuthError):
    '''Invalid request format
    '''
    pass


class InvalidScope(YandexOAuthError):
    '''App scope is changed after recieving verification code
    '''
    pass


class UnauthorizedClient(YandexOAuthError):
    '''Client is disable or not yet approved
    '''
    pass


class UnsupportedGrantType(YandexOAuthError):
    '''Unsupported grant_type value
    '''
    pass
