import requests

from configs import API_KEY


def get_weather(lat, lon):
    parameters = {
        'units': 'metric',
        'lang': 'ru'
    }
    data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}', params=parameters).json()
    return data
