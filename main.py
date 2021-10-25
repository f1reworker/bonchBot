import os
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import schedule

s=Service(ChromeDriverManager().install())

url = 'https://lk.sut.ru/cabinet/'
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
datas = {
    "users": "daniil.shalin2406@mail.ru",
    "parole": "fireworker"
}




def getSchedule():
    elementsArr = []
    driver = webdriver.Chrome(service = s, options = chrome_options)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        login.send_keys(datas["users"])
        driver.find_element(By.NAME,"parole").send_keys(datas["parole"])
        driver.find_element(By.NAME, "logButton").click()
        try:
            button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
        finally:
            button.click()
            try:
                sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
            finally:
                sch.click()
                try:
                    elements = driver.find_elements(By.PARTIAL_LINK_TEXT, "Кнопка")
                except NoSuchElementException:
                    elements = []
                finally:
                    if elements!=[]:
                        for elements in elements:
                            elementsArr.append(elements.text.split(" ")[3].replace(".", ""))
                        elementsArr = list(set(elementsArr)).sort()
                        driver.quit()
                        clickButton(elementsArr)
                print(elementsArr)


def click():
    driver = webdriver.Chrome(service = s, options = chrome_options)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        login.send_keys(datas["users"])
        driver.find_element(By.NAME, "parole").send_keys(datas["parole"])
        driver.find_element(By.NAME, "logButton").click()
        try:
            button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
        finally:
            button.click()
            try:
                sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
            finally:
                sch.click()
                i = 0
                while i<=30:
                    try:
                        driver.find_element(By.PARTIAL_LINK_TEXT, "Начать").click()
                    except NoSuchElementException:
                        time.sleep(300)
                        i+=5
                        driver.find_element(By.PARTIAL_LINK_TEXT, "Обновить").click()
                driver.quit()


def clickButton(elementsArr):
    for i in range(0, len(elementsArr)):
        lesson = elementsArr[i].split(":")
        timeLesson = str(int(lesson[0])-3)+":"+lesson[1]
        if len(timeLesson)==4:  timeLesson = "0"+timeLesson
        schedule.every().day.at(timeLesson).do(click)
        
schedule.every().day.at("22:35").do(getSchedule)
while True:
    schedule.run_pending()
    time.sleep(1)