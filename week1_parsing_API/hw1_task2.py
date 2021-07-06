import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv("../.env")

app_id = os.getenv("OPENWEATHER_KEY", None)


# получаем информацию о погоде в городе
def get_weather(city, app_id):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": app_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None


if __name__ == "__main__":
    city = input()
    weather = get_weather(city, app_id)
    pprint(weather)
