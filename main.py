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
import database
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


def click():
    while True:
        users = database.usersArr
        if users!=[]:
            for i in range(0, len(users)):
                thisUser = (db.child("Users").child(users[i]).get().val())
                #teacherandTime = db.child("Schedule").child(timeInt).child(users[i]).get().val().split("|")
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
                    print("Ошибка в логинации")
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
                                #if teacherandTime[0] and teacherandTime[1] in row.text:
                                try:
                                    row.find_element(By.PARTIAL_LINK_TEXT, "Начать").click()
                                except NoSuchElementException:
                                    driver.quit()
                                    pass
                                    break
                                else:
                                    print(login)
                                    db.child("Schedule Test").child(database.datetimeNow).update({users[i]:login})
                                    database.usersArr.remove(users[i])
                                    i-=1
                                    driver.quit()
                                    pass
                                    break
        else:   time.sleep(1)

def removeAndPushSchedule():
    database.usersArr = []
    db.child("Users Schedule").remove()
    db.child("Schedule").remove()
    pushSchedule()


def changeWeek():
    db.update({"Number Week": (db.child("Number Week").get().val()+1)})   

def getSchedule():
    i = database.count
    if i > 157:
        database.count = 0
        return schedule.CancelJob
    dateTimeNow = str(datetime.now().time())[:5]
    database.datetimeNow = dateTimeNow
    removeTime = str(int(dateTimeNow.split(":")[0])-1)+":" + dateTimeNow.split(":")[1]
    if len(removeTime)==4:  removeTime = "0"+ removeTime
    if "Schedule" in list(db.get().val().keys()):
        if dateTimeNow in list(db.child("Schedule").get().val().keys()):
            if db.child("Schedule").child(removeTime).get().val()!=None:
                for rT in list(db.child("Schedule").child(removeTime).get().val().keys()):
                    if rT in database.usersArr: database.usersArr.remove(rT)
            if db.child("Schedule").child(dateTimeNow).get().val()!=None:
                database.usersArr+=list(db.child("Schedule").child(dateTimeNow).get().val().keys())
            print(database.usersArr)
    database.count+=1

def startTimer():
    schedule.every(5).minutes.do(getSchedule)

def startThread():
    getScheduleThread = Thread(target=startTimer)
    getScheduleThread.start()

schedule.every().day.at("21:04").do(removeAndPushSchedule)
schedule.every().day.at("05:55").do(getSchedule)
schedule.every().sunday.at("21:00").do(changeWeek)


def runSchedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduleThread = Thread(target=runSchedule)
clickThread = Thread(target=click)
clickThread.start()
scheduleThread.start()