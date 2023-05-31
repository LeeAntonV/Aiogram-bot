import os 
import asyncio
import aiohttp
import datetime

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from dotenv import load_dotenv


def configure():
    load_dotenv()

def main():
    configure()
main()

router = Router()

bot_token = os.environ.get("API_KEY")
open_weather_token = os.environ.get("Weather_key")


@router.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.reply("Hi\nType name of the city and i will show you weather statistics")

@router.message()
async def get_weather(message: types.Message):
    async with aiohttp.ClientSession() as session:      
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
            r = await session.get(f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
            data = await r.json()
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


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(bot_token, parse_mode="HTML")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(get_weather(types.Message))
