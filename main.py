#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from telebot import TeleBot
from telebot import types
import json
from os import path


TOKEN = '5967901240:AAEHJhYqKpoZ1l7gv_NosAu50YNbIC9MK-I'

CHANNEL_ID = -1001783340499
FORWARDED_CHANNEL_ID = -1001899049651
CHANNEL_ID_FOR_URLS = "tomikbooks"


bot = TeleBot(TOKEN)

if path.exists("storage.json"):
    with open("storage.json", "r", encoding="UTF-8") as file:
        main_dict = json.load(file)
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


def analyse_message(message_text, entities, message_id):
    # print(message)
    if entities != None:
        message_entities = filter(lambda x: x.type == "hashtag", entities)
        hashtags = []
        for message_entity in message_entities:
            hashtags.append(message_text[message_entity.offset: message_entity.offset + message_entity.length])
        hashtags.sort(reverse=True)
        book_name = ""
        for hashtag in hashtags:
            if "Т_илл" in hashtag:
                name = " ".join(filter(lambda x: x != "", hashtag[6:].split("_")))
                main_dict["Иллюстраторы"][name] = f"https://t.me/{CHANNEL_ID_FOR_URLS}/{message_id}"
            elif "Т_кино" in hashtag:
                name = " ".join(filter(lambda x: x != "", hashtag[7:].split("_")))
                main_dict["Экранизации"][name] = f"https://t.me/{CHANNEL_ID_FOR_URLS}/{message_id}"
            elif "Т_соб" in hashtag:
                name = " ".join(filter(lambda x: x != "", hashtag[6:].split("_")))
                main_dict["События"][name] = f"https://t.me/{CHANNEL_ID_FOR_URLS}/{message_id}"
            elif "Т_лок" in hashtag:
                name = " ".join(filter(lambda x: x != "", hashtag[6:].split("_")))
                main_dict["Локации"][name] = f"https://t.me/{CHANNEL_ID_FOR_URLS}/{message_id}"
            elif "Т_кн" in hashtag:
                name = " ".join(filter(lambda x: x != "", hashtag[5:].split("_")))
                book_name = name
            elif "Т_авт" in hashtag:
                name = " ".join(filter(lambda x: x != "", hashtag[6:].split("_")))
                main_dict["Книги"]["Авторы"][name] = main_dict["Книги"]["Авторы"].get(name, {}) 
                main_dict["Книги"]["Авторы"][name].update({book_name: f"https://t.me/{CHANNEL_ID_FOR_URLS}/{message_id}"})
        with open("storage.json", "w", encoding="UTF-8") as file:
            json.dump(main_dict, file)


@bot.channel_post_handler(content_types=["text", "photo"])
@bot.edited_channel_post_handler()
def channel_hand(message: types.Message):
    message_text = ""
    entities = []
    if message.content_type == "text":
        message_text = message.text
        entities = message.entities
    else:
        message_text = message.caption
        entities = message.caption_entities
    # print("kkkkkkk")
    if message.sender_chat.id == CHANNEL_ID:
        analyse_message(message_text, entities, message.message_id)
    elif message.forward_from_chat != None and message.forward_from_chat.id == CHANNEL_ID and message.sender_chat.id == FORWARDED_CHANNEL_ID:
        # print(message)
        analyse_message(message_text, entities, message.forward_from_message_id)


@bot.message_handler(commands=["start"])
def search_hand(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    for key in main_dict.keys():
        btn1 = types.InlineKeyboardButton(text=key, callback_data=key)
        markup.add(btn1)
    bot.send_message(message.from_user.id, text="Выберите категорию:", reply_markup = markup, disable_web_page_preview=True)


@bot.callback_query_handler(func=lambda call: True)
def callback_hand(call: types.CallbackQuery):
    action = call.data
    msg = call.message
    if "Книги" not in action and "main" not in action:
        text = f"""<b>{action}:\n</b>"""
        for name, link in sorted(main_dict[action].items()):
            text += f'''<a href="{link}">{name}</a>\n'''
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Назад", callback_data="main"))
        bot.edit_message_text(text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)
    elif "Книги" in action:
        text = f"""<b>{action}:\n</b>"""
        for author, books in sorted(main_dict["Книги"]["Авторы"].items()):
            text += f'''{author}:\n'''
            for name, link in sorted(books.items()):
                text += f'''<a href="{link}">{name}</a>\n'''
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Назад", callback_data="main"))
        bot.edit_message_text(text, chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)
    elif "main" in action:
        markup = types.InlineKeyboardMarkup()
        for key in main_dict.keys():
            btn1 = types.InlineKeyboardButton(text=key, callback_data=key)
            markup.add(btn1)
        bot.edit_message_text("Выберите категорию:", chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=markup, disable_web_page_preview=True)


bot.polling(none_stop=True, interval=0)
