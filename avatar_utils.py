# -*- coding: utf-8 -*-
'''Yandex ID avatar utilites
'''


def get_avatar_url(avatar_id: str, size: str = 'islands-200') -> str:
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
        str: Avatar url
    '''
    return f'https://avatars.yandex.net/get-yapic/{avatar_id}/{size}'
