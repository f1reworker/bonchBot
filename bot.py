import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import config
token = Bot(token="2087293427:AAEqHp5QE7BK_7G8JNlDUdbhtKi9EqpMQdI")
bot = Dispatcher(token)
@bot.message_handler(commands="start")
async def cmd_test1(message: types.Message):
        await message.answer("Введите логин от лк")

@bot.message_handler(lambda message: message.text != "Да" and  message.text != "Нет")
async def cmd_test2(message: types.Message):
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
    await message.answer("Вы зарегистрированы!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(config.login + " " + config.password)

@bot.message_handler(lambda message: message.text == "Нет")
async def false(message: types.Message):
    config.login = ""
    config.password = ""
    await message.answer("Введите логин от лк", reply_markup=types.ReplyKeyboardRemove())

