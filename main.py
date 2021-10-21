
from selenium import webdriver
import schedule
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
datas = {
    "users": "daniil.shalin2406@mail.ru",
    "parole": "fireworker"
}
url = 'https://lk.sut.ru/cabinet/'
pathToExe = "C:/Users/danii/Downloads/chromedriver_win32/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")


def getSchedule():
    elementsArr = []
    driver = webdriver.Chrome(executable_path=pathToExe,options=chrome_options)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        login.send_keys(datas["users"])
        driver.find_element_by_name("parole").send_keys(datas["parole"])
        driver.find_element_by_name("logButton").click()
        try:
            button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
        finally:
            button.click()
            try:
                sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
            finally:
                sch.click()
                try: 
                    elements = WebDriverWait(driver, 1).until(EC.visibility_of_elements_located((By.PARTIAL_LINK_TEXT, "Кнопка")))
                finally:
                    for elements in elements:
                        elementsArr.append(elements.text.split(" ")[3].replace(".", ""))
                    elementsArr = set(elementsArr)
                    driver.quit()
                    clickButton(elementsArr)


def clickButton(elementsArr):
    i = 0
    for i in range(0, len(elementsArr)):
        # TODO: разобраться с shedule
        schedule.every().day.at(elementsArr[i]).do(click)


def click():
    driver = webdriver.Chrome(executable_path=pathToExe,options=chrome_options)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        login.send_keys(datas["users"])
        driver.find_element_by_name("parole").send_keys(datas["parole"])
        driver.find_element_by_name("logButton").click()
        try:
            button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
        finally:
            button.click()
            try:
                sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
            finally:
                sch.click()
                try:
                    button = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Начать"))
                )
                finally:
                    button.click()
                    driver.quit()

def testSch():
    driver = webdriver.Chrome(executable_path=pathToExe,options=chrome_options)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        login.send_keys(datas["users"])
        driver.find_element_by_name("parole").send_keys(datas["parole"])
        driver.find_element_by_name("logButton").click()
        try:
            button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
        finally:
            button.click()
            try:
                sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
            finally:
                sch.click()

def arr():
    elementsArr = ["20:15:58", "20:15", "20:16"]
    i = 0
    for i in range(0, len(elementsArr)):
        # TODO: разобраться с shedule
        schedule.every().day.at(elementsArr[i]).do(testSch)
schedule.every().day.at("8:00").do(getSchedule)
while True:
    schedule.run_pending()
    time.sleep(1)
