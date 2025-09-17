from time import sleep as pause
from random import randint
import json
import re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

from misc import terminate_driver


def parsing_category(driver, url):
    page = 1
    driver.get(url)
    pause(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    number_of_pages = 0
    span_tags = soup.find_all('span')
    for i in span_tags:
        if bool(str(i).find('data-role="items-count"') != -1):
            number_of_pages = [int(x) for x in str(i) if x.isdigit()]
    res = int(''.join(map(str, number_of_pages)))
    pages_total = (res // 18) + 1
    print(f'  • {pages_total} pages')
    urls = []
    true_url = url
    while True:
        page_urls = parsing_page(driver)
        print(f'    ◦ {page} page | amount of products: {len(page_urls)} | url: {url}')
        urls += page_urls
        if page >= pages_total:
            break
        page += 1
        url = true_url + f'?p={page}'
        error = True
        while error:
            try:
                driver.get(url)
                error = False
            except Exception:
                print(f'      - error during parsing {page} page, retrying...')
                error = True
                continue
        pause(randint(6, 9))
    print(f"    (amount of parsed products: {len(urls)})")
    return urls


def parsing_page(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    elements = soup.find_all('a', class_="catalog-product__name ui-link ui-link_black")
    ratings = soup.find_all('a', class_="catalog-product__rating")
    result = []
    for i, element in enumerate(elements):
        rating_amount_text = ratings[i].text.strip()
        if 'k' in rating_amount_text:
            rating_amount_text = re.sub('k', '', rating_amount_text)
            rating_amount = float(rating_amount_text) * 1000
        elif rating_amount_text == 'нет отзывов':
            rating_amount = 0
        else:
            try:
                rating_amount = int(rating_amount_text)
            except ValueError:
                rating_amount = 0
        if rating_amount >= 10:
            result.append('https://www.dns-shop.ru' + element.get("href"))
    return result


def parsing_product_urls():
    options = uc.ChromeOptions()
    options.add_argument("enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    driver = uc.Chrome(options=options, enable_cdp_events=True)
    with open("assets/urls/categories.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("Start parsing products...")
    products = {}
    for category in range(len(data)):
        print(f"{list(data.keys())[category]}:")
        products[list(data.keys())[category]] = parsing_category(driver, data[list(data.keys())[category]])
        with open("assets/urls/products.json", 'w', encoding='utf-8') as file:
            json.dump(products, file)
    terminate_driver(driver)
