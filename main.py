#!TODO: составление расписания с вечера, опрос про пары вечером

from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import schedule
from threading import Thread
from database import db
from parseSchedule import parseTable
from datetime import datetime

s=Service(ChromeDriverManager().install())

url = 'https://lk.sut.ru/cabinet/'
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


def pushSchedule():
    usersArr = db.child("Users").get().each()
    for i in range(0, len(usersArr)):
        user_id = usersArr[i].key()
        user = db.child("Users").child(user_id).get().val()
        parseTable(user, user_id)


def click(timeInt):
    userArr = db.child("Schedule").child(timeInt).get().val()
    while userArr!=None:
        userArr = db.child("Schedule").child(timeInt).get().val()
        if userArr!=None:
            user = list(db.child("Schedule").child(timeInt).get().val().keys())
            for i in range(0, len(user)):
                thisUser = (db.child("Users").child(user[i]).get().val())
                teacherandTime = db.child("Schedule").child(timeInt).child(user[i]).get().val().split("|")
                login = thisUser["login"]
                password = thisUser["password"]
                driver = webdriver.Chrome(service = s, options = chrome_options)
                driver.get(url)
                try:
                    loginArea = ""
                    loginArea = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.NAME, "users")))
                except Exception as e:
                    print("Except" + str(e))
                    driver.quit()
                    pass
                else:
                    loginArea.send_keys(login)
                    driver.find_element(By.NAME, "parole").send_keys(password)
                    driver.find_element(By.NAME, "logButton").click()
                    try:
                        button = ""
                        button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
                    except Exception as e:
                        print("Except" + str(e))
                        driver.quit()
                        pass
                    else:
                        button.click()
                        try:
                            sch = ""
                            sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
                        except Exception as e:
                            print("Except" + str(e))
                            driver.quit()
                            pass
                        else:
                            sch.click()
                            time.sleep(1)
                            rows = driver.find_elements(By.CSS_SELECTOR, '[style="background: #FF9933 !important "]')
                            for row in rows:
                                if teacherandTime[0] and teacherandTime[1] in row.text:
                                    try:
                                        row.find_element(By.PARTIAL_LINK_TEXT, "Начать").click()
                                    except NoSuchElementException:
                                        driver.quit()
                                        pass
                                        break
                                    else:
                                        print(login)
                                        db.child("Schedule").child(timeInt).child(user[i]).remove()
                                        driver.quit()
                                        pass
                                        break

def removeAndPushSchedule():
    db.child("Users Schedule").remove()
    db.child("Schedule").remove()
    pushSchedule()

def timer(thread, timeInt):
    thread.start()
    time.sleep(1150)
    db.child("Schedule").child(timeInt).remove()
    thread.join()

def runNewClick(timeInt, i):
    countI = i%4
    if countI==0:
        thread00 = Thread(target=click, args=(timeInt,))
        thread01 = Thread(target = timer, args=(thread00, timeInt,))
        thread01.start()
    elif countI==1:
        thread10 = Thread(target=click, args=(timeInt,))
        thread11 = Thread(target = timer, args=(thread10, timeInt,))
        thread11.start()
    elif countI==2:
        thread20 = Thread(target=click, args=(timeInt,))
        thread21 = Thread(target = timer, args=(thread20, timeInt,))
        thread21.start()
    elif countI==3:
        thread30 = Thread(target=click, args=(timeInt, timeInt,))
        thread31 = Thread(target = timer, args=(thread30, timeInt,))
        thread31.start()
    return schedule.CancelJob

def timerFiveMinutes():
    i = 0
    while i<133:
        getSchedule(i)
        time.sleep(300)
        i+=1

def changeWeek():
    db.update({"Number Week": (db.child("Number Week").get().val()+1)})   

def getSchedule(i):
    if "Schedule" in list(db.get().val().keys()):
        dateTimeNow = str(datetime.now().time())[:5]
        if dateTimeNow in list(db.child("Schedule").get().val().keys()):
            runNewClick(dateTimeNow, i)


def startTimer():
    timerThread = Thread(target=timerFiveMinutes)
    timerThread.start()


schedule.every().day.at("21:02").do(removeAndPushSchedule)
schedule.every().day.at("06:00").do(startTimer)
schedule.every().sunday.at("21:00").do(changeWeek)


def runSchedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
pushSchedule()
scheduleThread = Thread(target=runSchedule)
scheduleThread.start()