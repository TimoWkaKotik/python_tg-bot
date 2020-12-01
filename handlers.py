#Import library
from main import bot, dp
from aiogram import types
from aiogram.types import Message
from config import admin_id

#Send message to admin
async def send_to_admin(dp):
	await bot.send_message(chat_id=admin_id, text="Добро пожаловать, Господь Бог")

#Start bot using func
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	text = f'''Привет! {message.from_user.full_name} Это бот 🤖 🙌 Для работы бота в группе необходимо дать ему права администратора и включить все разрешения .'''
	await message.answer(text=text) 


