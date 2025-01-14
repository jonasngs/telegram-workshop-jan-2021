#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging

from mal import Anime, AnimeSearch
from mal.anime_search import AnimeSearchResult
from telebot import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

from api.telegram_api import send_message, bot
from beans.user import User
from handlers import animesearch

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# def sendKeyboard(user: User, queries) -> None:
#     queryCount = len(queries)
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
#     for x in range(queryCount):
#         malid = queries[x].mal_id
#         anime = Anime(malid)
#         markup.add(str(anime.title_english))
#         if x > 6:
#             break
#
#     bot.send_message(user.id, 'choose one', reply_markup=markup)
#     #print(update.callback_query)

def sendkeyboard(update: Update, user: User, queries) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Anime", callback_data='1'),
            InlineKeyboardButton("Manga", callback_data='2'),
        ],
        [InlineKeyboardButton("Web Comics", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data[-4:] == 'info':
        handle_info(query)

    elif query.data[-5:] == 'genre':
        handle_genre(query)

    elif query.data[-8:] == 'synopsis':
        synopsis_command(query.data[:-9], query)

    elif query.data[-5:] == 'image':
        image_command(query.data[:-6], query)

    elif query.data[-4:] == 'rank':
        rank_command(query.data[:-5], query)

    elif query.data[-8:] == 'duration':
        duration_command(query.data[:-9], query)

    elif query.data[-8:] == 'air date':
        air_date_command(query.data[:-9], query)

    elif query.data[-6:] == 'status':
        status_command(query.data[:-7], query)

    else:
        keyboard = [
            [InlineKeyboardButton('info', callback_data=query.data + ' info')],
            [InlineKeyboardButton('genre', callback_data=query.data + ' genre')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text='Choose one: ', reply_markup=reply_markup)


def handle_info(query):
    anime = query.data[:-5]
    keyboard = [
        [InlineKeyboardButton('image', callback_data=anime + ' image')],
        [InlineKeyboardButton('synopsis', callback_data=anime + ' synopsis')],
        [InlineKeyboardButton('rank', callback_data=anime + ' rank')],
        [InlineKeyboardButton('duration', callback_data=anime + ' duration')],
        [InlineKeyboardButton('air date', callback_data=anime + ' air date')],
        [InlineKeyboardButton('status', callback_data=anime + ' status')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text='Choose one:', reply_markup=reply_markup)

    #else:
     #   anime = AnimeSearch(int(query.data))
      #  query.edit_message_text(text=f"{anime.title} is rated: {anime.score}")
        #query.edit_message_text(text=f"Selected option: {query.data}")


def handle_genre():
    return ''


def synopsis_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' synopsis:\n' + Anime(res).synopsis)


def rank_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' rank:\n' + str(Anime(res).rank))


def duration_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' duration:\n' + Anime(res).duration)


def air_date_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' air date:\n' + Anime(res).aired)


def status_command(res, query):
    query.edit_message_text(text=Anime(res).title + ' status:\n' + Anime(res).status)


def image_command(res, query):
    bot.send_photo(query.id, res.image_url)

    
def echo(update, context, args):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def startUpdater():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1561103971:AAEr8QvFWgfKVwhDihLrhnO6mr0TnXGc-04", use_context=True)




