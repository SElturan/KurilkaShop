from handlers.main import BotMain
from aiogram.types import Message
from aiogram import executor
from config import dp 



bot = BotMain()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)