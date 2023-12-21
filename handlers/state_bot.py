import re
from datetime import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import dp, bot
from aiogram.types import Message, Contact
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .keyboards import get_keyboard
from database.database import user_post, check_user, patch_phone
from .text import rules_text




class Registration:
    def __init__(self,message: Message):
        self.message = message
        
    async def registration_user(self, message:Message):
        class RegistrationState(StatesGroup):
            first_name = State()
            last_name = State()
            age = State()
            phone = State()

        await RegistrationState.first_name.set()
        await message.answer('Пожалуйста, введите ваше имя для регистрации.', reply_markup=ReplyKeyboardRemove())

        @dp.message_handler(state=RegistrationState.first_name)
        async def first_name_state(message: Message, state: FSMContext):
            async with state.proxy() as data:
                data['first_name'] = message.text
                await state.update_data(first_name=message.text)  # Сохранение first_name в состояние
                await message.answer('Введите вашу фамилию.')
                await RegistrationState.next()


        @dp.message_handler(state=RegistrationState.last_name)
        async def last_name_state(message: Message, state: FSMContext):
            async with state.proxy() as data:
                data['last_name'] = message.text
            await message.answer('Введите год рождения в формате ДД.ММ.ГГГГ (например, 01.01.2001).')
            await RegistrationState.next()

        @dp.message_handler(state=RegistrationState.age)
        async def age_state(message: Message, state: FSMContext):
            async with state.proxy() as data:
                try:
                    birthdate = datetime.strptime(message.text, "%d.%m.%Y")
                    today = datetime.today()
                    age = today.year - birthdate.year
                    if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
                        age -= 1
                    data['age'] = age
                    data['date'] = message.text  # Сохраняем дату рождения
                except ValueError:
                    return await message.answer('Неверный формат данных!\nПожалуйста, введите год рождения в формате ДД.ММ.ГГГГ (например, 01.01.2001).')

            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(KeyboardButton("Отправить номер телефона📱", request_contact=True))
            await message.answer(text='Подтвердите номер телефона', reply_markup=keyboard)
            await RegistrationState.next()

        @dp.message_handler(content_types=types.ContentType.CONTACT, state=RegistrationState.phone)
        async def phone_state(message: Message, state: FSMContext):
            async with state.proxy() as data:
                data['phone'] = message.contact.phone_number
                await state.update_data(phone=message.contact.phone_number)  # Сохранение phone в состояние
                first_name = data['first_name']
                last_name = data['last_name']
                age = data['age']
                phone = data['phone']

                formatted_text = f"*Имя:* {first_name}\n*Фамилия:* {last_name}\n*Возраст:* {age}\n*Телефон:* {phone}"

                await message.answer(formatted_text, parse_mode=types.ParseMode.MARKDOWN)

                await message.answer("Все ли данные верны? Да / Нет", reply_markup=get_keyboard('yes/no'))

        @dp.message_handler(lambda message: message.text.lower() == 'да', state=RegistrationState)
        async def confirmation_yes(message: types.Message, state: FSMContext):
            user_data = await state.get_data()
            nick = message.from_user.first_name
            user_id = message.from_user.id
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            age = user_data.get('age')
            date = user_data.get('date')
            phone = user_data.get('phone')
            data = {
                "nickname": nick,
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone,
                "age": age,
                "date": date,
            }
            post = await user_post(data)
            if post:
                text = rules_text()
                await message.answer(f"Поздравляю! Ваша регистрация успешно завершена\n{text}", \
                                     reply_markup=(get_keyboard('menu')))
            await state.finish()


        @dp.message_handler(lambda message: message.text.lower() == 'нет', state=RegistrationState)
        async def confirmation_no(message: types.Message, state: FSMContext):
            await message.answer("Хорошо, начнем регистрацию заново.", reply_markup=ReplyKeyboardRemove())
            await RegistrationState.first_name.set()
            await message.answer('Пожалуйста, введите ваше имя для регистрации.')






class AddPhone:
    def __init__(self, message: Message):
        self.message = message
        
    async def add_list_phone(self, message: Message):
        class AddPhoneState(StatesGroup):
            phone = State()

        await AddPhoneState.phone.set()
        user_id = message.from_user.id
        look_user_get = await check_user(user_id)

        await message.answer('Введите номер телефона в формате: +7XXXXXXXXXX\n'
                     'Пример: +79991234567', reply_markup=ReplyKeyboardRemove())

        @dp.message_handler(state=AddPhoneState.phone)
        async def phone_state(message: Message, state: FSMContext):
            async with state.proxy() as data:
                data['phone'] = message.text
                if look_user_get[0]['phone_number'] and look_user_get[0]['phone_number2']:
                    await message.answer('У вас уже имеется два номера', reply_markup=get_keyboard('menu'))
                    await state.finish()
                    return

                phone = data['phone']
                user_id = message.from_user.id
                
                # Проверка корректности номера телефона
                phone_pattern = r'^\+7\d{10}$'  # Паттерн для российского номера
                if not re.match(phone_pattern, phone):
                    await message.answer('Введите номер телефона в формате: +7XXXXXXXXXX\n'
                     'Пример: +79991234567', reply_markup=get_keyboard('main_menu'))

                    return

                patch_user_phone = await patch_phone(user_id, phone)
                if patch_user_phone:
                    await message.answer(f'Вы успешно добавили номер телефона!', reply_markup=get_keyboard('menu'))
                else:
                    await message.answer('Ошибка при добавлении номера телефона', reply_markup=get_keyboard('menu'))
                await state.finish()
