from time import sleep as pause
import os
import re
import csv
import json
import undetected_chromedriver as uc
import requests

from misc import clean_comment, characteristicGrades_for_text, create_csv, terminate_driver


def parsing_product(driver, url):
    error = True
    while error:
        try:
            driver.get(url)
            pause(10)
            error = False
        except Exception:
            print(f'    ◦ error during parsing {url}, retrying...')
            error = True
            continue
    page_source = driver.page_source
    pattern = re.compile(r'(/product/microdata/.*?/)')
    match = pattern.search(page_source)
    if match:
        part_of_url = str(match.group(1))
        driver.get(f"https://www.dns-shop.ru{part_of_url}")
        page_source = driver.page_source
        name = re.search(r'"name":"(.*?)",', page_source).group(1)
        description = re.search(r'"description":"(.*?)",', page_source).group(1)
        reviewCount = int(re.search(r'"reviewCount":(.*?)},', page_source).group(1)) - 4
        offset = 3
        no_text_reviews = False
        while True:
            if reviewCount <= 0 or no_text_reviews:
                break
            data = {"objectId": part_of_url[19:-1], "offset": offset, "limit": 10}
            res = requests.post("https://www.dns-shop.ru/opinion/opinions/get/", data=data, timeout=3000)
            if res.status_code == 200:
                reviews = res.json()['data']['opinions']
                with open("assets/dns_data.csv", mode="a", encoding='utf-8') as file:
                    writer = csv.writer(file)
                    for review in reviews:
                        if review['plus'] is None and review['minus'] is None and review['comment'] is None:
                            no_text_reviews = True
                            break
                        writer.writerow([
                            f"Название:{name}",
                            f"Описание: {description}",
                            f"Рейтинг: {review['rating']}",
                            f"Достоинства: {clean_comment(review['plus'])}, Недостатки: {clean_comment(review['minus'])},"
                            f" Комментарий: {clean_comment(review['comment'])}",
                            f"Характеристики: [{characteristicGrades_for_text(review['characteristicGrades'])[:-1]}]"
                        ])
                reviewCount -= 10
                offset += 10
            else:
                print("Error: ", res.status_code)
    else:
        print("'/product/microdata/' not found in page_source")


def parsing_reviews():
    if not os.path.exists("assets/dns_data.csv"):
        create_csv()
    options = uc.ChromeOptions()
    options.add_argument("enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = uc.Chrome(options=options, enable_cdp_events=True)
    with open("assets/urls/products.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("Start parsing reviews...")
    for category in range(len(data)):
        print(f"{list(data.keys())[category]}:")
        for url in range(len(data[list(data.keys())[category]])):
            print(f"  • {url + 1} product | url: {data[list(data.keys())[category]][url]}")
            parsing_product(driver, data[list(data.keys())[category]][url])
    terminate_driver(driver)
