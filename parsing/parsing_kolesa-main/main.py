import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tabulate import tabulate

driver = webdriver.Chrome()

start_page = 1356
current_page = start_page
card_counter = 1

# Открываем CSV-файл для добавления данных
with open("kolesa_data2.csv", "a", encoding="utf-8", newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Проверяем, пуст ли файл (нет ли заголовков)
    if csvfile.tell() == 0:
        # Записываем заголовок в CSV-файлы
        csv_writer.writerow(["Card"])

    while True:
        url = f"https://kolesa.kz/cars/avtokredit/astana/?={current_page}"
        driver.get(url)

        try:
            wait = WebDriverWait(driver, 10)

            parent_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "a-list")))

            cards = parent_element.find_elements(By.CLASS_NAME, "a-list__item")

            if not cards:
                print(f"Данных нету {current_page}.")
                break

            for card in cards:
                card_data = card.text.split('\n')

                # Форматируем карточку
                formatted_card = f"""-{card_counter}-\nTitle: {card_data[0]}\nPrice: {card_data[1]}\nDescription: {card_data[2]}\nPrice per month: {card_data[3]}\nPlace and date: {card_data[4]}"""

                # Записываем отформатированную карточку в файл
                csvfile.write(formatted_card)
                csvfile.write("\n\n")

                card_counter += 1

            print(f"Данные из страницы {current_page}.")
            current_page += 1

        except TimeoutException:
            print(f"Время ожидания страницы истекло {current_page}. Выход.")
            break

driver.quit()