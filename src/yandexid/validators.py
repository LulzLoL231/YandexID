# -*- coding: utf-8 -*-
'''Yandex ID API data validators
'''
import warnings

from .errors.yandexoauth import (
    InvalidDeviceID, InvalidDeviceName
)


class DeviceID:
    '''Device ID validator
    '''
    @staticmethod
    def validate(device_id: str) -> bool:
        '''Validate device ID

        Args:
            device_id (str): Device ID

        Returns:
            bool: True if device ID is valid, False otherwise
        '''
        if len(device_id) < 6:
            raise InvalidDeviceID('Device ID is too short')
        if len(device_id) > 50:
            raise InvalidDeviceID('Device ID is too long')
        if not device_id.isalnum():
            raise InvalidDeviceID('Device ID must contain only alphanumeric characters')
        return True


class DeviceName:
    '''Device name validator
    '''
    @staticmethod
    def validate(device_name: str) -> bool:
        '''Validate device name

        Args:
            device_name (str): Device name

        Returns:
            bool: True if device name is valid, False otherwise
        '''
        if len(device_name) > 100:
            raise InvalidDeviceName('Device name is too long')
        return True


class OptionalScope:
    '''Optional scope validator
    '''
    @staticmethod
    def validate(scope: str, optional_scope: str):
        '''Validate optional scope

        Args:
            scope (str): OAuth scope
            optional_scope (str): Optional scope
        '''
        ignored_scope: list[str] = []
        for scope_item in optional_scope.split(','):
            if scope_item not in scope:
                ignored_scope.append(scope_item.strip())
        if ignored_scope:
            warnings.warn(
                f'Optional scopes {", ".join(ignored_scope)} is not in scope.',
                UserWarning
            )
