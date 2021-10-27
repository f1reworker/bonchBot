from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import config
s=Service(ChromeDriverManager().install())

url = 'https://lk.sut.ru/cabinet/'
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")





def getSchedule(user):
    elementsArr = []
    driver = webdriver.Chrome(service = s, options = chrome_options)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        login.send_keys(user["login"])
        driver.find_element(By.NAME,"parole").send_keys(user["password"])
        driver.find_element(By.NAME, "logButton").click()
        try:
            button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
        finally:
            button.click()
            try:
                sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
            finally:
                sch.click()
                time.sleep(2)
                elements = driver.find_elements(By.PARTIAL_LINK_TEXT, "Кнопка")
                if elements!=[]:
                    for elements in elements:
                        elementsArr.append(elements.text.split(" ")[3].replace(".", ""))
                    elementsArr = list(set(elementsArr))
                    #clickButton(elementsArr)
            driver.quit()
            print(elementsArr)


def click():
    driver = webdriver.Chrome(service = s, options = chrome_options)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        #login.send_keys(datas["users"])
        #driver.find_element(By.NAME, "parole").send_keys(datas["parole"])
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
                        driver.find_element(By.PARTIAL_LINK_TEXT, "начала от").click()
                driver.quit()


def clickButton(elementsArr):
    for i in range(0, len(elementsArr)):
        lesson = elementsArr[i].split(":")
        timeLesson = str(int(lesson[0])-3)+":"+lesson[1]
        if len(timeLesson)==4:  timeLesson = "0"+timeLesson
        print(timeLesson)
        schedule.every().day.at(timeLesson).do(click)

def arrSchedule():
    for i in range(0, len(config.users)):
        getSchedule(config.users[i])

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

#while True:
#    schedule.run_pending()
#    time.sleep(1)