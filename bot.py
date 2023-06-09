#Импорты
import asyncio
import sqlite3 as sql
import random

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types.input_file import InputFile

from aiogram.types.message import ContentType

from config import TOKEN
import config
from db import DataBase
import datetime

#Модель бота и клас диспетчер
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

admin_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("add_ban_word", callback_data="add_ban_word"),
                                           InlineKeyboardButton("remove_ban_word", callback_data="remove_ban_word"))

class add_ban_state(StatesGroup):
    text = State()

@dp.message_handler(commands=['start'])
async def start_command(message : types.Message):
    if message.chat.type != "private":
        kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Личка создателя", url="https://t.me/iuda194"),
                                        InlineKeyboardButton("Я на гит хабе", url="https://github.com/IUDA194/harakiriii_bot"),
                                        InlineKeyboardButton("Мой сайт", url="naeb.online"))
        await bot.send_message(message.chat.id, "Привет, я бот харакири! Подробности отправил в лс")
        await bot.send_photo(message.from_user.id, open("img.jpg", "rb") ,"Привет, я бот написанный @iuda194 за 3 часа что-бы предотвратить спам, для списка всех моих команд введи /команды")
        await asyncio.sleep(2)
        await bot.send_message(message.from_user.id, "Если хочешь добавить меня в группу напиши моему создвтелю в лс, так же можешь сам склонить мой проект с гита", reply_markup=kb)
    elif message.chat.type == "private":
        await message.delete()
        kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Личка создателя", url="https://t.me/iuda194"),
                                        InlineKeyboardButton("Я на гит хабе", url="https://github.com/IUDA194/harakiriii_bot"),
                                        InlineKeyboardButton("Мой сайт", url="naeb.online"))
        await bot.send_photo(message.from_user.id, open("img.jpg", "rb") ,"Привет, я бот написанный @iuda194 за 3 часа что-бы предотвратить спам")
        await asyncio.sleep(2)
        await bot.send_message(message.from_user.id, "Если хочешь добавить меня в группу напиши моему создвтелю в лс, так же можешь сам склонить мой проект с гита", reply_markup=kb)

@dp.message_handler(commands=['enter', 'ентер', "задать_чат"])
async def start_command(message : types.Message):
    if message.chat.type != "private":
        a = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if a['status'] == "creator":
            if not DataBase.select_chat(message.chat.id)["status"]:
                DataBase.insert_chat(message.chat.id, message.from_user.id)
                await bot.send_message(message.chat.id, f"""<b>Бум!</b>\n<i>harakiriii зарегестрировал ваш сервер</i>\n<i>У всех учасников чата создан аккаунт в системе бота</i><code> /start</code> <i>в личку боту для его открытия</i>
    Имя чата в памяти бота {message.chat.id} <i>Вы всегда можете сменить его личнов кабинете</i>""")
            else:
                await bot.send_message(message.chat.id, "Бот уже зареган")
        else:
            await bot.send_message(message.chat.id, "Эту команду должен вводить только владелец чата")
        await message.delete()
    elif message.chat.type == "private":    
        await bot.send_message(message.chat.id, "Эту команду нужно написать в группе которую хочешь подключить к боту")

@dp.message_handler(commands=['admin'])
async def start_command(message : types.Message):
    if message.chat.type == "private":
        if message.chat.id == 687899499:
            await bot.send_message(687899499, "Админка", reply_markup=admin_kb)

@dp.message_handler(commands=['mute', "мут"], is_chat_admin=True)
async def mute(message : types.Message):
    if message.chat.type != "private":
        #if message.from_user.id == 687899499:
        if not message.reply_to_message:
            await message.reply("Эта команда должна быть ответом на сообщение!")
            return
        try:
            mute_text = config.muts_texts[random.randrange(0, len(config.muts_texts))]
            muteint = int(message.text.split()[1])
            mutetype = message.text.split()[2]
            comment = " ".join(message.text.split()[3:])
        except IndexError:
            mute_text = config.muts_texts[random.randrange(0, len(config.muts_texts))]
            muteint = 240
            mutetype = "m"
            comment = " ".join(message.text.split()[3:])
        if mutetype == "ч" or mutetype == "часов" or mutetype == "час":
            dt = datetime.datetime.now() + datetime.timedelta(hours=muteint)
            timestamp = dt.timestamp()
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
            await message.reply(mute_text)
        elif mutetype == "м" or mutetype == "минут" or mutetype == "минуты" or mutetype == "m":
            dt = datetime.datetime.now() + datetime.timedelta(minutes=muteint)
            timestamp = dt.timestamp()
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
            await message.reply(mute_text)
        elif mutetype == "д" or mutetype == "дней" or mutetype == "день":
            dt = datetime.datetime.now() + datetime.timedelta(days=muteint)
            timestamp = dt.timestamp()
            await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
            await message.reply(mute_text)

@dp.message_handler(commands=['unmute', "анмут"], is_chat_admin=True)
async def mute(message : types.Message):
    if message.chat.type != "private":
        #if message.from_user.id == 687899499:
        if not message.reply_to_message:
            await message.reply("Эта команда должна быть ответом на сообщение!")
            return
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(True))
        await message.reply(config.unmuts_texts[random.randrange(0, len(config.muts_texts))])

@dp.message_handler(commands=["команды", "command"])
async def mute(message : types.Message):
    kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Личка создателя", url="https://t.me/iuda194"))
    if message.chat.type != "private":
        a = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if a['status'] == "creator" or a['status'] == "administrator":
            await message.reply("Поведал в личке)")
            await bot.send_message(message.from_user.id, config.text_command, reply_markup=kb)
        else:
            await message.reply("У тебя нет прав бро)")
    else:
        await bot.send_message(message.from_user.id, config.text_command,reply_markup=kb)

@dp.callback_query_handler(text="add_ban_word")
async def process_buy_command(callback_query: types.CallbackQuery):
    await add_ban_state.text.set()
    await bot.send_message(callback_query.from_user.id, "enter text")

@dp.message_handler(state=add_ban_state.text)
async def start_command(message : types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Ban word was added")
    DataBase.insert_ban_word(message.text)
    await state.finish()

async def anti_flood(*args, **kwargs):
    message = args[0] 
    message : types.Message
    if message.chat.type != "private":
        dt = datetime.datetime.now() + datetime.timedelta(minutes=5) 
        await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = dt)
        await message.reply("Нахуй флудить | Мут на 5 минут")


@dp.message_handler(content_types=ContentType.ANIMATION)
async def start_command(message : types.Message):
    user_chat_data = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user_chat_data['status'] != "creator" and user_chat_data['status'] != "administrator":
        us_data = DataBase.select_user(message.from_user.id)
        if len(us_data) >= 1:
            if us_data["data"]["last_text"] == "GIF1":
                dt = datetime.datetime.now() + datetime.timedelta(hours=1) 
                await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = dt)
                await message.reply("Нахуй гифки | Мут на час")
            if us_data["data"]["last_text"] == "GIF":
                dt = datetime.datetime.now() + datetime.timedelta(hours=1) 
                DataBase.update_last_text(message.from_user.id, "GIF1")
            else:
                DataBase.update_last_text(message.from_user.id, "GIF")

@dp.message_handler()
@dp.throttled(anti_flood, rate=0.7) #rate это количество секунд, при котором входящие сообщения считаются флудом.
async def start_command(message : types.Message):
    if message.chat.type != "private":
        user_chat_data = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if user_chat_data['status'] != "creator" and user_chat_data['status'] != "administrator":
            # if len(message.text) <= 5:
            #     await message.reply(f"@{message.from_user.username} У тебя что налог на буквы? | Отдохни 30 секунд")
            #     dt = datetime.datetime.now() + datetime.timedelta(seconds=30)  
            #     await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = dt)
            #     await message.delete()
            try:
                us_data = DataBase.select_user(message.from_user.id)
                if len(us_data) >= 1:
                    ban_woeds = DataBase.select_ban_word()
                    for i in ban_woeds['ban_words']:
                        if i[0] in message.text:
                            DataBase.update_last_text(message.from_user.id, message.text)
                            await message.delete()
                            await bot.send_message(message.chat.id, f"@{message.from_user.username} | Твоё сообщение удалено, приоритет понижен на 1")
                            DataBase.update_rep(message.from_user.id, -1)
                    if us_data["data"]["last_text"] == message.text:
                        status = DataBase.update_rep(message.from_user.id, -1)["status"]
                        if status == True:
                            pass
                        elif status == False:
                            dt = datetime.datetime.now() + datetime.timedelta(hours=6) 
                            await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = dt)
                            await message.reply("В мут обезьяну | Мут на 6 часов")
                    else:
                        DataBase.update_rep(message.from_user.id, 1)
                        DataBase.update_last_text(message.from_user.id, message.text)
                else:
                    DataBase.insert_user(chat_id = message.from_user.id, name=message.from_user.first_name)
                    ban_woeds = DataBase.select_ban_word()
                    for i in ban_woeds['ban_words']:
                        if i[0] in message.text:
                            DataBase.update_last_text(message.from_user.id, message.text)
                            await message.delete()
                            await bot.send_message(message.chat.id, f"@{message.from_user.username} | Твоё сообщение удалено, приоритет понижен на 1")
                            DataBase.update_rep(message.from_user.id, -1)
                    if us_data["data"]["last_text"] == message.text:
                        status = DataBase.update_rep(message.from_user.id, -1)["status"]
                        if status == True:
                            pass
                        elif status == False:
                            dt = datetime.datetime.now() + datetime.timedelta(hours=6)  
                            await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = dt)
                            await message.reply("В мут обезьяну | Мут на 6 часов")
                    else:
                        DataBase.update_rep(message.from_user.id, 1)
                        DataBase.update_last_text(message.from_user.id, message.text)
            except: pass

#Функция которая запускается со стартом бота
async def on_startup(_):
    print('bot online')
#Пулинг бота
executor.start_polling(dp,skip_updates=True, on_startup=on_startup) #Пуллинг бота

#Вывод уведомления про отключение бота
print("Bot offline")
#                                                                                                           Coded by Iuda with Love...