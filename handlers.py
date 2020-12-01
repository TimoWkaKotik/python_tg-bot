#Import library
from main import bot, dp
from aiogram import types
from aiogram.types import Message
from config import admin_id
import pymysql
from config import dbHost, dbUser, dbPassword, dbName

#DB connection
connection = pymysql.Connect(dbHost, dbUser, dbPassword, dbName)

#Keyboard
keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)
arr_keyboard = ['btn1', 'btn2']

#Send message to admin
async def send_to_admin(dp):
	await bot.send_message(chat_id=admin_id, text="Добро пожаловать, Господь Бог. Напиши /start, чтобы посмотреть мои навыки")


#Start bot function
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	keyboard_markup.add(*(types.KeyboardButton(text) for text in arr_keyboard))
	await message.answer(text='Привет! Потестим кнопки', reply_markup=keyboard_markup)
	analytic(message.from_user.username, message.from_user.id, message.from_user.full_name, message.text)

#Send data to DB MySQL
def analytic(nickname, tgid, fullname, command):
	cursor = connection.cursor()
	cursor.execute("INSERT INTO users(user_nickname, user_tgid, user_fullname, user_command) VALUES('%s','%s','%s','%s')" % (nickname, tgid, fullname, command))
	connection.commit()
	cursor.close()
