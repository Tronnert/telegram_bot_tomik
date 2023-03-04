from telebot import TeleBot
from telebot import types
import json
from os import path


TOKEN = '5967901240:AAEHJhYqKpoZ1l7gv_NosAu50YNbIC9MK-I'

CHANNEL_ID = -1001899049651
CHANNEL_ID_FOR_URLS = 1899049651


bot = TeleBot(TOKEN)

if path.exists("storage.json"):
    with open("storage.json", "r", encoding="UTF-8") as file:
        main_dict = json.load(file)
        print(main_dict)
else:
    main_dict = {
                "Книги": 
                    {
                    "Авторы": {}, # Т_авт_Прокофьева (внутри тоже дикты) # Т_кн_Лоскутик_и_облако
                    },
                "Иллюстраторы": 
                    {
                        # Т_илл_фамилия # Т_илл_Сутеев
                    },
                "Экранизации": 
                    {
                        # Т_кино_назв # Т_кино_Маугли
                    },
                "События": 
                    {
                        # Т_соб_назв # Т_соб_ярмарка_в_Крупской
                    },
                "Локации": 
                    {
                        # Т_лок_назв # Т_лок_Литературные_мостки
                    }
                }


def analyse_message(message):
    message_entities = filter(lambda x: x.type == "hashtag", message.entities)
    hashtags = []
    for message_entity in message_entities:
        hashtags.append(message.text[message_entity.offset: message_entity.offset + message_entity.length])
    hashtags.sort(reverse=True)
    book_name = ""
    for hashtag in hashtags:
        if "Т_илл" in hashtag:
            name = " ".join(filter(lambda x: x != "", hashtag[6:].split("_")))
            main_dict["Иллюстраторы"][name] = f"https://t.me/c/{CHANNEL_ID_FOR_URLS}/{message.message_id}"
        elif "Т_кино" in hashtag:
            name = " ".join(filter(lambda x: x != "", hashtag[7:].split("_")))
            main_dict["Экранизации"][name] = f"https://t.me/c/{CHANNEL_ID_FOR_URLS}/{message.message_id}"
        elif "Т_соб" in hashtag:
            name = " ".join(filter(lambda x: x != "", hashtag[6:].split("_")))
            main_dict["События"][name] = f"https://t.me/c/{CHANNEL_ID_FOR_URLS}/{message.message_id}"
        elif "Т_лок" in hashtag:
            name = " ".join(filter(lambda x: x != "", hashtag[6:].split("_")))
            main_dict["Локации"][name] = f"https://t.me/c/{CHANNEL_ID_FOR_URLS}/{message.message_id}"
        elif "Т_кн" in hashtag:
            name = " ".join(filter(lambda x: x != "", hashtag[5:].split("_")))
            # main_dict["Книги"]["Названия"][name] = f"https://t.me/c/{CHANNEL_ID_FOR_URLS}/{message.message_id}"
            book_name = name
        elif "Т_авт" in hashtag:
            # print(hashtag[6:])
            name = " ".join(filter(lambda x: x != "", hashtag[6:].split("_")))
            main_dict["Книги"]["Авторы"][name] = main_dict["Книги"]["Авторы"].get(name, {}) | {book_name: f"https://t.me/c/{CHANNEL_ID_FOR_URLS}/{message.message_id}"}
    with open("storage.json", "w", encoding="UTF-8") as file:
        json.dump(main_dict, file)


@bot.channel_post_handler()
@bot.edited_channel_post_handler()
def channel_hand(message):
    if message.sender_chat.id == CHANNEL_ID:
        analyse_message(message)
        # bot.send_message(message.sender_chat.id, " ".join(map(str, hashtags)))
        # print(main_dict)


@bot.message_handler(commands=["start"])
def search_hand(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    for key in main_dict.keys():
        btn1 = types.InlineKeyboardButton(text=key, callback_data=key)
        markup.add(btn1)
    bot.send_message(message.from_user.id, text="Выберите категорию:", reply_markup = markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_hand(call: types.CallbackQuery):
    action = call.data
    msg = call.message
    if "Книги" not in action and "main" not in action:
        text = f"""{action}:\n"""
        for name, link in sorted(main_dict[action].items()):
            text += f'''<a href="{link}">{name}</a>\n'''
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Назад", callback_data="main"))
        bot.edit_message_text(text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="HTML", reply_markup=markup)
    elif "Книги" in action:
        text = f"""{action}:\n"""
        for author, books in sorted(main_dict["Книги"]["Авторы"].items()):
            text += f'''{author}:\n'''
            for name, link in sorted(books.items()):
                text += f'''<a href="{link}">{name}</a>\n'''
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Назад", callback_data="main"))
        bot.edit_message_text(text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="HTML", reply_markup=markup)
    elif "main" in action:
        markup = types.InlineKeyboardMarkup()
        for key in main_dict.keys():
            btn1 = types.InlineKeyboardButton(text=key, callback_data=key)
            markup.add(btn1)
        bot.edit_message_text("Выберите категорию:", chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=markup)


bot.polling(none_stop=True, interval=0)
