from aiogram import Bot, Dispatcher, types
import config
import time
from database import addUser


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


s=Service(ChromeDriverManager().install())
url = 'https://lk.sut.ru/cabinet/'
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


token = Bot(token="2087293427:AAEqHp5QE7BK_7G8JNlDUdbhtKi9EqpMQdI")
bot = Dispatcher(token)
@bot.message_handler(commands="start")
async def start(message: types.Message):
    config.login = ""
    config.password = ""
    await message.answer("Введите логин от лк", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(lambda message: message.text != "Да" and  message.text != "Нет"  and  message.text != "Хуй" and  message.text != "Сева хуй")
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
    await message.answer("Проверка...")
    if checkAuth(config.login, config.password):
        addUser(user_id=message.from_user.id, login = config.login, password = config.password)
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

@bot.message_handler(lambda message: message.text == "Хуй")
async def zxc(message: types.Message):
    await message.reply("Сам хуй")

@bot.message_handler(lambda message: message.text == "Сева хуй")
async def zxc(message: types.Message):
    await message.reply("Полностю согласен!")




def checkAuth(loginUser, passwordUser):
    driver = webdriver.Chrome(service = s, options = chrome_options)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        login.send_keys(loginUser)
        driver.find_element(By.NAME,"parole").send_keys(passwordUser)
        driver.find_element(By.NAME, "logButton").click()
        time.sleep(0.5)
        try: 
            driver.find_element(By.CLASS_NAME, "lm_item")
        except UnexpectedAlertPresentException:
            driver.quit()
            return False
        else:
            driver.quit()
            return True