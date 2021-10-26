from aiogram import Bot, Dispatcher, types, executor
import config
import main
token = Bot(token="2087293427:AAEqHp5QE7BK_7G8JNlDUdbhtKi9EqpMQdI")
bot = Dispatcher(token)
@bot.message_handler(commands="start")
async def start(message: types.Message):
    config.login = ""
    config.password = ""
    user_id = message.from_user.id
    await message.answer("Введите логин от лк", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(lambda message: message.text != "Да" and  message.text != "Нет")
async def auth(message: types.Message):
    if config.login!="":
        config.password = message.text
        await message.answer(config.login + " " + config.password)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Да", "Нет"]
        keyboard.add(*buttons)
        await message.answer("Все верно?", reply_markup=keyboard)
    if config.login == "":
        config.login = message.text
        await message.answer("Введите пароль от лк")

@bot.message_handler(lambda message: message.text == "Да")
async def true(message: types.Message):
    if main.checkAuth(config.login, config.password):
        await message.answer("Вы зарегистрированы!", reply_markup=types.ReplyKeyboardRemove())
    else: 
        config.login = "" 
        config.password = ""
        keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = ["/start"]
        keyboards.add(*button)
        await message.answer("Введенные данные неверны!", reply_markup=keyboards)

@bot.message_handler(lambda message: message.text == "Нет")
async def false(message: types.Message):
    config.login = ""
    config.password = ""
    await message.answer("Введите логин от лк", reply_markup=types.ReplyKeyboardRemove())

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(bot, skip_updates=True)

