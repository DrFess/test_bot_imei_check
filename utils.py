import re

import requests

from settings import WHITE_LIST, API_TOKEN


def validate_imei(imei: str) -> bool:
    imei_pattern = re.compile(r'^\d{15}$')
    return bool(imei_pattern.match(imei))


def is_user_allowed(user: int) -> bool:
    return user in WHITE_LIST


def authentication():

    url = "https://api.imeicheck.net/v1/account"

    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    return response.json()


