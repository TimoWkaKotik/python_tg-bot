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
from config import API_TOKEN

bot = Bot(API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
	firstname = State()
	lastname = State()
	group = State()
	startedu = State()

#Bot start
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
	await Form.firstname.set()
	await message.reply("Привет! Как тебя зовут?")

#Ask name
@dp.message_handler(state=Form.firstname)
async def process_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['firstname'] = message.text
	await Form.next()
	await message.reply("Какая y тебя фамилия?")

#Ask lastname
@dp.message_handler(state=Form.lastname)
async def process_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['lastname'] = message.text
	await Form.next()
	await message.reply("В какой группе ты учишься?")

#Ask group 
@dp.message_handler(state=Form.group)
async def process_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['group'] = message.text
	await Form.next()

#Ask year
years = ["2017", "2018", "2019", "2020"]

@dp.message_handler(lambda message: message.text, state=Form.group)
async def process_age(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['group'] = message.text
	await Form.next()

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add(types.KeyboardButton(text) for text in years)

	await message.reply("В каком году ты поступил?", reply_markup=markup)

#Check year
@dp.message_handler(lambda message: message.text not in years, state=Form.startedu)
async def process_gender_invalid(message: types.Message):
	return await message.reply("Ответ неверный. Выберите нужный вариант на клавиатуре.")


#Poll result
@dp.message_handler(state=Form. startedu)
async def process_gender(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['startedu'] = message.text

		markup = types.ReplyKeyboardRemove()

		await bot.send_message(
		message.chat.id,
		md.text(
			md.text('Рад познакомиться,', md.bold(data['firstname'] + " " + data['lastname'])),
			md.text('Твоя группа:', data['group']),
			md.text('Начал обучение в:', data['startedu']),
			sep='\n',
		),
		reply_markup=markup,
		parse_mode=ParseMode.MARKDOWN,
	)
	await state.finish()


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False)
