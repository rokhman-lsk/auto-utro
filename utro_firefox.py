import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


URL = os.getenv('URL')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')

NUMBER_OF_CONTRACT = os.getenv('NUMBER_OF_CONTRACT')  # Tele2
DESCRIPTION = 'Документация и написание скриптов для Netbox'
HOURS = 8


def click(by, el):
    WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((by, el))).click()


"""Скрытие окна браузера"""
opts = webdriver.FirefoxOptions()
opts.headless = False  # Чтобы скрыть - True
"""Инициализация"""
driver = webdriver.Firefox(options=opts)
driver.implicitly_wait(15)
driver.get(URL)
"""Аутентификация"""
driver.find_element(By.NAME, 'username').send_keys(LOGIN)
driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
click(By.XPATH, '//input[@value="Войти"]')
time.sleep(15)  # Для двухфакторной (чтобы ввести числа), чтобы ее не было, следует подключиться к VPN
"""Заполнение недельного отчета в УТРО"""
# Получение чисел (даты) понедельника и пятницы
date = driver.find_element(By.XPATH, '//span[contains(text(), "-")]')
monday_date = int(date.text[0:2])
friday_date = int(date.text[-5:-3]) - 2
# Добавление контракта
click(By.XPATH, '//button[text()="Добавить активность"]')
driver.find_element(By.XPATH, '//input[@placeholder="Для поиска введите текст"]').send_keys(NUMBER_OF_CONTRACT)
click(By.XPATH, '//span[text()="Действующие контракты"]')
click(By.XPATH, '//button[text()="Добавить"]')
# Списание трудозатрат
click(By.XPATH, '//div[@class="dropdown"]/div')
click(By.XPATH, '//a[text()="Списать за период"]')
driver.find_elements(By.XPATH, '//div[@role="button"]')[1].click()
click(By.XPATH, f'//li[contains(text(), "{monday_date}")]')
driver.find_elements(By.XPATH, '//div[@role="button"]')[2].click()
click(By.XPATH, f'//li[contains(text(), "{friday_date}")]')
driver.find_element(By.XPATH, '//textarea[@placeholder="Введите описание"]').send_keys(DESCRIPTION)
driver.find_element(By.XPATH, '//input[@placeholder="0"]').send_keys(HOURS)
click(By.XPATH, '//button[text()="Списать трудозатраты"]')
click(By.XPATH, '//button[text()="Отправить отчет"]')
time.sleep(5)  # Для того, чтобы убедиться в заполнении
# Выход из учетной записи
click(By.XPATH, '//a[@href="/logout"]')
print('Отчет по трудозатратам списан')
