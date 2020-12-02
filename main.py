import aiogram.utils.markdown as md
from aiogram import types
from aiogram.types import Message

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from config import API_TOKEN, dbHost, dbUser, dbPassword, dbName
import csv, datetime, pymysql

bot = Bot(API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


#data to DB
# def stat(user_id, command):
# 	connection = pymysql.Connect(dbHost, dbUser, dbPassword, dbName)
# 	cursor = connection.cursor()
# 	cursor.execute("INSERT INTO users(user_id, user_command, date) VALUES('%s','%s','%s')" % (user_id, command, date))
# 	connection.commit()
# 	cursor.close()

#data to CSV
def statistics (user_id, command):
	date = datetime.date.today().strftime("%d-%m-%Y %H:%M")
	with open('data.csv', 'a', newline="") as fil:
		wr = csv.writer(fil, delimiter=';')
		wr.writerow([date, user_id, command])

#start func
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
	await message.reply("Привет!")
	statistics(message.chat.id, message.text)
	# stat(message.chat.id, message.text)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False)
