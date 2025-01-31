import asyncio
import json
import logging
import os

import requests
from aiogram import Bot, Router, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from utils import validate_imei, is_user_allowed

bot = Bot(token=os.getenv('TOKEN'))
router = Router()


@router.message(Command(commands=['start', 'menu']))
async def command_start_handler(message: Message):
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        await message.reply('Извините, у вас нет доступа к этому боту.')
        return
    await message.answer('Привет! Отправь мне IMEI (только цифры)')


@router.message(lambda message: is_user_allowed(message.from_user.id) and validate_imei(message.text))
async def get_imei_info(message: Message):
    imei = message.text

    headers = {
        'Authorization': f'Bearer {os.getenv('API_TOKEN')}',
        'Content-Type': 'application/json'
    }

    body = json.dumps({
        'deviceId': imei,
        'serviceId': 12
    })

    response = requests.post(os.getenv('IMEI_CHECK_API_URL'), headers=headers, data=body)
    result = response.json()
    answer = f'Модель: {result.get("properties").get("deviceName")}\n{result.get("properties").get("image")}'
    await message.answer(answer)


async def main():
    dp = Dispatcher()
    dp.include_routers(
        router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
