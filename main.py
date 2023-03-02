from telebot import TeleBot
from telebot import types

bot = TeleBot('5967901240:AAEHJhYqKpoZ1l7gv_NosAu50YNbIC9MK-I')


@bot.message_handler()
def url(message):
    # markup = types.InlineKeyboardMarkup()
    # btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://habr.com/ru/all/')
    # markup.add(btn1)
    # bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на сайт хабра", reply_markup = markup)
    bot.send_message(message.from_user.id, message)


bot.polling(none_stop=True, interval=0) 