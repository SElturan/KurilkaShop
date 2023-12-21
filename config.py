from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

http_api = 'http://31.129.97.107:8000'
CHANNEL_ID = '@kurilka_shop_spb'
TOKEN = '5864205073:AAHLMIsgWaOdkKcMqxWbFJiYFqcnjJJf8Zs'
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

