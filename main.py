from re import S
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


s=Service(ChromeDriverManager().install())

url = 'https://lk.sut.ru/cabinet/'
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")





def findSchedule(user):
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
                        lesson = elements.text.split(" ")[3].replace(".", "").split(":")
                        timeLesson = str(int(lesson[0])-3)+":"+lesson[1]
                        if len(timeLesson)==4:  timeLesson = "0"+timeLesson
                        elementsArr.append(timeLesson)
                driver.quit()
                return elementsArr

def pushSchedule():
    db.child("Schedule").remove()
    db.child("Users Schedule").remove()
    usersArr = db.child("Users").get().each()
    for i in range(0, len(usersArr)):
        user_id = usersArr[i].key()
        user = db.child("Users").child(user_id).get().val()
        parseTable(user, user_id)
        timeSched = findSchedule(user)
        if timeSched!=None:
            for q in range (0, len(timeSched)):
                if timeSched[q]==timeSched[q-1]:
                    lesson = timeSched[q].split(":")
                    timeLesson = lesson[0]+":"+str(int(lesson[1])+5)
                    db.child("Schedule").child(timeLesson).child(user_id).set(False)
                else:
                    db.child("Schedule").child(timeSched[q]).child(user_id).set(False)
    getSchedule()
def click(timeInt):
    userArr = db.child("Schedule").child(timeInt).get().val()
    while userArr!=None:
        userArr = db.child("Schedule").child(timeInt).get().val()
        if userArr!=None:
            user = list(db.child("Schedule").child(timeInt).get().val().keys())
            for i in range(0, len(user)):
                thisUser = (db.child("Users").child(user[i]).get().val())
                login = thisUser["login"]
                password = thisUser["password"]
                driver = webdriver.Chrome(service = s, options = chrome_options)
                driver.get(url)
                try:
                    loginArea = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.NAME, "users")))
                finally:
                    loginArea.send_keys(login)
                    driver.find_element(By.NAME, "parole").send_keys(password)
                    driver.find_element(By.NAME, "logButton").click()
                    try:
                        button = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "lm_item")))
                    finally:
                        button.click()
                        try:
                            sch = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.LINK_TEXT, "Расписание")))
                        finally:
                            sch.click()
                            time.sleep(1)
                            try:
                                driver.find_element(By.PARTIAL_LINK_TEXT, "Начать").click()
                            except NoSuchElementException:
                                driver.quit()
                                pass
                            else:
                                print(login)
                                db.child("Schedule").child(timeInt).child(user[i]).remove()
                                driver.quit()

def timer(thread):
    thread.start()
    time.sleep(2300)
    thread.join()

def runNewClick(timeInt, i):
    countI = i%8
    if countI==0:
        thread00 = Thread(target=click, args=(timeInt,))
        thread01 = Thread(target = timer, args=(thread00,))
        thread01.start()
    elif countI==1:
        thread10 = Thread(target=click, args=(timeInt,))
        thread11 = Thread(target = timer, args=(thread10,))
        thread11.start()
    elif countI==2:
        thread20 = Thread(target=click, args=(timeInt,))
        thread21 = Thread(target = timer, args=(thread20,))
        thread21.start()
    elif countI==3:
        thread30 = Thread(target=click, args=(timeInt,))
        thread31 = Thread(target = timer, args=(thread30,))
        thread31.start()
    elif countI==4:
        thread40 = Thread(target=click, args=(timeInt,))
        thread41 = Thread(target = timer, args=(thread40,))
        thread41.start()
    elif countI==5:
        thread50 = Thread(target=click, args=(timeInt,))
        thread51 = Thread(target = timer, args=(thread50,))
        thread51.start()
    elif countI==6:
        thread60 = Thread(target=click, args=(timeInt,))
        thread61 = Thread(target = timer, args=(thread60,))
        thread61.start()
    elif countI==7:
        thread70 = Thread(target=click, args=(timeInt,))
        thread71 = Thread(target = timer, args=(thread70,))
        thread71.start()
    return schedule.CancelJob


def getSchedule():
    if "Schedule" in list(db.get().val().keys()):
        timeArr = list(db.child("Schedule").get().val().keys())
        for i in range(0, len(timeArr)):
            schedule.every().day.at(timeArr[i]).do(runNewClick, timeArr[i], i)

schedule.every().day.at("21:10").do(pushSchedule)
def runSchedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
pushSchedule()
scheduleThread = Thread(target=runSchedule)
scheduleThread.start()