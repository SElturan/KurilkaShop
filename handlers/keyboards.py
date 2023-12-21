from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup



def get_keyboard(name: str):

    if name == 'menu':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Сгенерировать код'),
                             KeyboardButton('Показать баллы'))
        keyboard.add(KeyboardButton('Постоянный клиент'),
                             KeyboardButton('Филлиалы'))
        keyboard.add(KeyboardButton('Правила'),
                             KeyboardButton('Тех.поддержка'))
   

    elif name == 'yes/no':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Да'),
                             KeyboardButton('Нет'))
    elif name == 'subs_kb':
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='Подписаться 👍', url='https://t.me/dksopdkakda'))
        keyboard.add(InlineKeyboardButton(text='Проверить 🔍', callback_data='check_sub'))

    elif name == 'continue':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Продолжить'),
                             KeyboardButton('Назад'))
    elif name == 'delete_roles':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Отказаться от постоянного клиента'))
        keyboard.add(KeyboardButton('Назад'))
        
    elif name == 'main_menu':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(KeyboardButton('Назад'))
        
    return keyboard