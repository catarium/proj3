import requests
from app.core.settings import settings


def get_location_key(city):
    params = {
            'apikey': settings.API_KEY,
            'q': city
            }
    res = requests.get('http://dataservice.accuweather.com/locations/v1/cities/search', params=params)
    if res.status_code != 200:
        print('Ошибка', res.status_code, res.text)
        return False
    res = res.json()
    if not res:
        return []
    return res


def get_weather(location_key):
    params = {
            'apikey': settings.API_KEY,
            'details': True,
            'language': 'ru-RU',
            'metric': True
            }
    res = requests.get(f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}', params=params)
    if res.status_code != 200:
        print('Ошибка', res.status_code, res.text)
        return False
    res = res.json()
    return res
