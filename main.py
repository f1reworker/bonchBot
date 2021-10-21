
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
def openSite(driver):
    driver.get(url)
    driver.find_element_by_name("users").send_keys(datas["users"])
    driver.find_element_by_name("parole").send_keys(datas["parole"])
    driver.find_element_by_name("logButton").click()
    time.sleep(3)
    driver.find_element_by_class_name("lm_item").click()
    driver.find_element_by_class_name("l_menu_a").click()
def getSchedule():
    driver = webdriver.Chrome(executable_path=pathToExe,options=chrome_options)
    elementsArr = []
    openSite(driver)
    time.sleep(1)
    elements = driver.find_elements_by_partial_link_text("Кнопка")
    for elements in elements:
        elementsArr.append(elements.text.split(" ")[3].replace(".", ""))
    print(elementsArr)
    driver.quit()
    clickButton(elementsArr, driver)
def clickButton(elementsArr, driver):
    i = 0
    for i in range(0, len(elementsArr)):
        # TODO: разобраться с shedule
        schedule.every().day.at(elementsArr[i]).do(click(driver))
def click(driver):
    openSite(driver)
    try:
        button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "Начать"))
    )
    finally:
        button.click()
        driver.quit()
schedule.every().day.at("03:08").do(getSchedule)
while True:
    schedule.run_pending()
    time.sleep(10)

