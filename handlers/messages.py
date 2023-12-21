async def check_sub_channel(chat_id):
    if chat_id['status'] != 'left':
        return True

    else:
        return False
    


async def subs_channel(message,bot, channel_id):
        user_id = message.from_user.id
        is_subscribed = await bot.get_chat_member(channel_id, user_id)
        check_sub_user = await check_sub_channel(is_subscribed)
        return check_sub_user