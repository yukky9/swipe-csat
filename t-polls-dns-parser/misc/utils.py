import csv


def create_csv():
    with open("assets/dns_data.csv", mode="w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Имя", "Описание", "Рейтинг", "Комментарий", "Характеристики"]
        )


def terminate_driver(driver):
    driver.close()
    driver.quit()
