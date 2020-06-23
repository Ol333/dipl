#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pip install -U aiogram

# http://t.me/SPaCCE_info_bot
# token 927556733:AAEC8n5phWD7vkkhGqMtF-2e-K5LF6cbpEQ
# url = "https://api.telegram.org/927556733:AAEC8n5phWD7vkkhGqMtF-2e-K5LF6cbpEQ/"

import logging
import asyncio
import sys
import threading
from aiogram import Bot, Dispatcher, executor, types
from socket import gethostname
from datetime import timedelta

class BotThread(threading.Thread):
    def __init__(self, ac):
        threading.Thread.__init__(self)
        self.daemon = True
        self.ac = ac
    def run(self):
        print ("Thread ", self.ac.base_addr)
        set_ac(self.ac)

# # однократный асинхронный вызов bot.send_message при завершении модуля/проекта
#     def periodic(self,current_mod_name):
#         for id in chat_ids:
#             asyncio.run(bot.send_message(id,
#                                   str(current_mod_name)+' finished with code 0',
#                                   disable_notification=True))

API_TOKEN = '927556733:AAEC8n5phWD7vkkhGqMtF-2e-K5LF6cbpEQ'
logging.basicConfig(level=logging.INFO) # Configure logging
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
chat_ids = {}

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    chat_ids[message.from_user.id] = message.from_user
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns_text = ('/status', '/help', '/stop')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    await message.reply(("Привет! Я SPaCCEbot. Используй команду /status,"
                 + " чтобы посмотреть что сейчас запущено на ") + gethostname() + "; "
                 + "используйте команду /stop, чтобы остановить выполнение текущего проекта.",
                 reply_markup=keyboard_markup)

# узнать статус выполнения проекта
@dp.message_handler(commands=['status'])
async def send_status(message: types.Message):
    """
    This handler will be called when user sends `/status`
    """
    mas = ac.get_bot_info()
    current_run_time = mas[0]
    current_proj_name = mas[1]
    current_mod_name = mas[2]
    current_err_count = mas[3]
    if current_proj_name:
        await message.reply(gethostname() + ' выполняет ' + current_proj_name + ' ' + current_mod_name)
        await message.answer('Ошибок в проекте: ' + str(current_err_count))
        await message.answer('Проект выполняется уже: ' + str(current_run_time))
    else:
        await message.reply('Ничего не запущено...')
    print("status")

@dp.message_handler(commands=['stop'])
async def send_status(message: types.Message):
    """
    This handler will be called when user sends `/stop`
    """
    mas = ac.stop_project()
    await message.reply('Выполнение проекта остановлено.')

def set_ac(cur_ac):
    global ac
    ac = cur_ac
    executor.start_polling(dp, skip_updates=True)
