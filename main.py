from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
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
                    time.sleep(2)
                    elements = driver.find_elements_by_partial_link_text("Кнопка")
                finally:
                    for elements in elements:
                        elementsArr.append(elements.text.split(" ")[3].replace(".", ""))
                    elementsArr = list(set(elementsArr)).sort()
                    driver.quit()
                    clickButton(elementsArr)
                    print(elementsArr)


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
                i = 0
                while i<=20:
                    try:
                        driver.find_element_by_partial_link_text("Начать").click()
                    except NoSuchElementException:
                        time.sleep(300)
                        i+=5
                        driver.find_element_by_partial_link_text("Обновить").click()
                driver.quit()


def clickButton(elementsArr):
    i = 0
    lessonTime = []
    for i in range(0, len(elementsArr)):
        lesson = elementsArr[i].split(":")
        lessonTime.append(int(lesson[0])*3600+int(lesson[1])*60-10800)
        if i==0:
            time.sleep(lessonTime[i]-28800)
            click()
        if i!=0:
            time.sleep(lessonTime[i]-lessonTime[i-1]-30600)
            click()




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
                i = 0
                while i<=30:
                    try:
                        driver.find_element_by_partial_link_text("Начать").click()
                    except NoSuchElementException:
                        time.sleep(300)
                        i+=5
                        driver.find_element_by_partial_link_text("Обновить").click()
    time.sleep((30-i)*60)