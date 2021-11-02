from selenium import webdriver
from database import db
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
s=Service(ChromeDriverManager().install())

url = 'https://lk.sut.ru/cabinet/'
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

def parseTable(user, user_id):   
    driver = webdriver.Chrome(service = s, options = chrome_options)
    driver.get(url)
    try:
        login = ""
        login = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.NAME, "users")))
    finally:
        login.send_keys(user["login"])
        driver.find_element(By.NAME,"parole").send_keys(user["password"])
        driver.find_element(By.NAME, "logButton").click()
        try:
            button = ""
            button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
        finally:
            button.click()
            try:
                sch = []
                sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
            finally:
                sch.click()
                time.sleep(1)
                try:
                    rows = []
                    rows = driver.find_elements(By.CSS_SELECTOR, '[style="background: #FF9933 !important "]')
                except NoSuchElementException:
                    driver.quit()
                    return None
                else:
                    key = ""
                    i = 0
                    mCArr = []
                    for row in rows:
                        matrixColumn = []
                        column = row.find_elements(By.TAG_NAME, "td")
                        for col in column:
                            matrixColumn.append(col.text)
                        db.child("Users Schedule").child(user_id).child(key).update({i: matrixColumn})
                        i+=1
                        timeLesson = matrixColumn[0].split("-")[0].split("(")[-1].replace(".", ":")
                        if len(timeLesson)==4:  timeLesson = "0"+timeLesson
                        mCArr.append(timeLesson)
                    driver.quit() 
                    return mCArr





def parseAllTable(user, user_id):
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
                table = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="rightpanel"]/div/table/tbody')))
                rows = table.find_elements(By.TAG_NAME, "tr")
                key = ""
                for row in rows:
                    matrixColumn = []
                    column = row.find_elements(By.TAG_NAME, "td")
                    if len(column)==1:
                        key = column[0].text.split("\n")[1].replace(".", "-")
                    else:
                        for col in column:
                            matrixColumn.append(col.text.replace("\n", " "))
                        db.child("Users Schedule").child(user_id).child(key).update({str(matrixColumn.pop(0).replace(".", ":")+" "+matrixColumn.pop(-2).replace(".", ":")): str(matrixColumn)})
