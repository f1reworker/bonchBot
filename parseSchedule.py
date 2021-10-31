from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
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

def parseTable(user):
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
                print(table.text.split("\n"))
#parseTable({"login": "daniil.shalin2406@mail.ru", "password": "fireworker"})

t = [0, 1, 2, 3, 4, 5]
print(t[-1])
