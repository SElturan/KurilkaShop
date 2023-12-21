import random
import datetime
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup 
from config import dp, bot, CHANNEL_ID
from database.database import check_user, check_code_exists, code_post, regular_user_post, \
check_user_roles, delete_regular_user, get_branches, get_regular_info
from .state_bot import Registration, AddPhone
from .keyboards import get_keyboard
from .messages import subs_channel
from .text import *


class BotMain:
    def __init__(self):
        dp.register_message_handler(self.start,commands=['start'])
        dp.register_message_handler(self.random_code,text = 'Сгенерировать код')
        dp.register_message_handler(self.support,text = 'Тех.поддержка')
        dp.register_message_handler(self.phone_command,text = 'Добавить телефон')
        dp.register_message_handler(self.points,text = 'Показать баллы')
        dp.register_message_handler(self.regular_user,text = 'Постоянный клиент')
        dp.register_message_handler(self.rules,text = 'Правила')
        dp.register_message_handler(self.continue_roles,text = 'Продолжить')
        dp.register_message_handler(self.delete_roles,text = 'Отказаться от постоянного клиента')
        dp.register_message_handler(self.back,state='*',text = 'Назад')
        dp.register_message_handler(self.fillial,text = 'Филлиалы')
        dp.register_callback_query_handler(self.callback, lambda c: c.data in ['check_sub'])


    async def start(self, message: Message):
        user_id = message.from_user.id
        look_user_get = await check_user(user_id)
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        if look_user_get:
            await message.answer('Привет! Это бот для скидок.\nВыбери действие', reply_markup=get_keyboard('menu'))
        else:
            registration = Registration(message)
            await registration.registration_user(message)

    
    async def random_code(self, message: Message):
        user_id = message.from_user.id
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        check_role = await check_user_roles(user_id)
        if check_role:
            return await message.answer('Вы не можете генерировать код. \nЧтобы генерировать код вы должны отказаться от постоянного клиента\nНажмите на кнопку "Постоянный клиент"', reply_markup=get_keyboard('menu'))
        while True:
            code = random.randint(10000, 99999)  # Генерация случайного 5-значного кода
            
            # Проверка уникальности кода в базе данных
            if await check_code_exists(code):
                await message.answer(f"Код: {code}\nСообщите его продавцу!")
                data = {
                    "user_id": message.from_user.id,
                    "code": code
                }
                check_code = await code_post(data)
                if check_code:
                    await message.answer(f"Выберите действие")
                    break



    async def support(self, message: Message):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        
        url = InlineKeyboardMarkup()
        url.add(InlineKeyboardButton(text='Тех.поддержка 📞', url='https://t.me/Bams_06'))
        await message.answer(support(),reply_markup=url)

    
    async def phone_command(self, message: Message):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        add_phone = AddPhone(message)
        await add_phone.add_list_phone(message)
    

    async def callback(self, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        look_user_get = await check_user(user_id)  # Проверка наличия пользователя в базе данных
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(callback_query, bot, CHANNEL_ID)
        if not check_cub:
            return await callback_query.message.reply(not_sub(), reply_markup=kb)
        if look_user_get:
            await callback_query.message.answer('Привет! Это бот для скидок.\nВыбери действие',\
                                                reply_markup=get_keyboard('menu'))
        else:
            registration = Registration(callback_query.message)
            await registration.registration_user(callback_query.message)


    async def points(self, message: Message):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        user_id = message.from_user.id
        look_user_get = await check_user(user_id)
        points_user = look_user_get[0]['points']
        if points_user:
            await message.answer(f'У вас баллов: {points_user}')
        else:
            await message.answer('У вас баллов: 0')


    
    async def regular_user(self, message: Message):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)

        user_id = message.from_user.id
        check_role = await check_user_roles(user_id)
        if check_role:
            info_regular = await get_regular_info(user_id)
            response = "Вы уже являетесь постоянным клиентом.\nЧтобы отказаться от постоянного клиента нажмите на кнопку 'Отказаться от постоянного клиента'\n\n"
            for info in info_regular:
                response += f"<b>Сумма покупки::</b> {info['summ']}\n"
                response += f"<b>Процент скидки:</b> {info['discount']} %\n"
                response += f"<b>Посещений:</b> {info['visits']}"
            await message.answer(response,reply_markup=get_keyboard('delete_roles'), parse_mode='HTML')
        else:
            await message.answer('Хочешь стать нашим постоянным клиентом и получать все преимущества?\
                            \nОднако, для этого у тебя не будет доступа к генерации кода.\
                            \nТы уверен, что хочешь стать постоянным клиентом?', reply_markup=get_keyboard('continue'))




    async def continue_roles(self, message: Message):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        user_id = message.from_user.id
        post_regular_user = await regular_user_post(user_id)
        if post_regular_user:
            await message.answer('Поздравляем! Вы стали постоянным клиентом.', reply_markup=get_keyboard('menu'))
        else:
            await message.answer('Вы уже являетесь постоянным клиентом.', reply_markup=get_keyboard('menu'))


    async def rules(self, message: Message):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        text = rules_text()
        await message.answer(text)

    
    async def back(self, message: Message, state: FSMContext):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        current_state = await state.get_state()

            # Проверяем, есть ли текущее состояние
        if current_state is not None:
            await state.finish()
            await message.answer('Главное меню')
            await message.answer('Выберите действие', reply_markup=get_keyboard('menu'))
        else:
            await message.answer('Главное меню')
            await message.answer('Выберите действие', reply_markup=get_keyboard('menu'))     
    

    async def delete_roles(self, message: Message):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        user_id = message.from_user.id
        check_role = await check_user_roles(user_id)
        if not check_role:
            return await message.answer('Вы не являетесь постоянным клиентом', reply_markup=get_keyboard('menu'))
        delete_user = await delete_regular_user(user_id)
        if delete_user:
            await message.answer('Вы отказались от постоянного клиента. Теперь у вас есть доступ к генерации кода',\
                                 reply_markup=get_keyboard('menu'))
        else:
            await self.back(message)

    
    async def fillial(self, message: Message):
        kb = get_keyboard('subs_kb')
        check_cub = await subs_channel(message, bot, CHANNEL_ID)
        if not check_cub:
            return await message.reply(not_sub(), reply_markup=kb)
        branches = await get_branches()
        if branches:
            response = "<b>Вот список наших филиалов:</b>\n\n"
            for branch in branches:
                response += f"<b>Филиал:</b> {branch['name']}\n"
                response += f"<b>Локация:</b> {branch['location']}\n"
                
                opening_time = datetime.datetime.strptime(branch['opening_time'], "%H:%M:%S").strftime("%H:%M")
                closing_time = datetime.datetime.strptime(branch['closing_time'], "%H:%M:%S").strftime("%H:%M")
                
                response += f"<b>Время работы:</b> {opening_time} - {closing_time}\n\n"
            await message.answer(response, parse_mode='HTML')
        else:
            await message.answer("К сожалению, филиалы еще не добавлены. Ожидайте обновлений в ближайшее время!",\
                                parse_mode='HTML')