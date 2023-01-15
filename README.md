# Яндекс ID (OAuth) API
Библиотека для работы с API Яндекс ID (OAuth) для Python 3.10+.
Поддерживает асинхронную работу.

[Документация API](https://yandex.ru/dev/id/doc/dg/index.html)

## Установка

1. С помощью pip:
    
    ```bash
    pip install yandexid
    ```

2. С помощью pip+git:
    
    ```bash
    pip install https://github.com/LulzLoL231/yandexid.git
    ```

3. Из исходников:

    ```bash
    git clone https://github.com/LulzLoL231/yandexid
    pip install ./yandexid
    ```

## Пример использования

1. Получение OAuth токена:

    ```python
    from yandexid import YandexOAuth

    yandex_oauth = YandexOAuth(
        client_id='<client_id>',
        client_secret='<client_secret>',
        redirect_uri='<redirect_uri>'
    )
    auth_url = yandex_oauth.get_authorization_url()
    # Тут нужно перейти по ссылке auth_url и получить код авторизации
    token = yandex_oauth.get_token_from_code('<code>')
    ```
    Возвращает объект `Token` с информацией о OAuth токене. Формат объекта совпадает с [форматом ответа из API Яндекс ID](https://yandex.ru/dev/id/doc/dg/oauth/reference/console-client.html#console-client__token-body-title).


2. Получение информации о пользователе:

    ```python
    from yandexid import YandexID

    yandex_id = YandexID('<oauth_token>')
    user_info = yandex_id.get_user_info_json()
    ```
    Возвращает объект `User` с информацией о пользователе. Формат объекта совпадает с [форматом ответа из API Яндекс ID](https://yandex.ru/dev/id/doc/dg/api-id/reference/response.html).

## Асинхронная работа
Чтобы использовать асинхронность, используйте классы `AsyncYandexOAuth` и `AsyncYandexID`:

```python
from yandexid import AsyncYandexID

yandex_id = AsyncYandexID('<oauth_token>')
user_info = await yandex_id.get_user_info_json()
```
Название методов полностью совпадает с названием синхронных методов, не забывайте использовать `await` перед вызовом асинхронных методов.

Логотипы Яндекс ID и название сервиса "Яндекс ID" принадлежат Яндексу.
