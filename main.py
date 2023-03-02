from telebot import TeleBot
# from telebot import types
import re


TOKEN = '5967901240:AAEHJhYqKpoZ1l7gv_NosAu50YNbIC9MK-I'

CHANNEL_ID = -1001899049651

bot = TeleBot(TOKEN)


def extract_hashtags(s):
    return " ".join(re.findall(r"#(\w+)", s))


# @bot.message_handler()
@bot.channel_post_handler()
def url(message):
    # markup = types.InlineKeyboardMarkup()
    # btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://habr.com/ru/all/')
    # markup.add(btn1)
    # bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на сайт хабра", reply_markup = markup)
    # bot.send_message(message.from_user.id, message)
    if message.sender_chat.id == CHANNEL_ID:
    # print(message.sender_chat)
        bot.send_message(message.sender_chat.id, extract_hashtags(message.text))


bot.polling(none_stop=True, interval=0)