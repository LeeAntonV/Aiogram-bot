import os 
import datetime
import requests

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv


def configure():
    load_dotenv()

def main():
    configure()
main()


bot_token = os.environ.get("API_KEY")
open_weather_token = os.environ.get("Weather_key")


bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start','help'])
async def start_command(message: types.Message):
    await message.reply("Hi\nType name of the city and i will show you weather statistics")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Bright \U00002600",
        "Clouds": "Cloudy \U00002601",
        "Rain": "Rain \U00002614",
        "Drizzle": "Rain \U00002614",
        "Thunderstorm": "Thunderstorm \U000026A1",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B"
    }
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = " "

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Weather in city: {city}\nTempreture: {cur_weather}C° {wd}\n"
              f"Humidity: {humidity}%\nPressure: {pressure} mm of merc \nWind: {wind} m/s\n"
              f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nDay's Duration: {length_of_the_day}\n"
              f"***Goodbye!***"
              )
    except Exception as error:
        await message.reply("\U0001F534 Wrong city name \U0001F534")

if __name__ == '__main__':
    executor.start_polling(dp)