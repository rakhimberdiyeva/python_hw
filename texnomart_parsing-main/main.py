
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

URL = "https://texnomart.uz/ru/katalog/"
HOST = "https://texnomart.uz"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

def get_soup(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_categories():
    soup = get_soup(URL)
    categories = soup.find_all("a", class_="content__link")
    data = [
        {
            "title": category.text.strip(),
            "link": HOST + category.get("href"),
        }
        for category in categories
    ]
    return  data

def get_pagination(link):
    soup = get_soup(link)
    pagination = soup.find("div", class_="pagination")
    if pagination is None:
        return 1
    buttons = pagination.select('button[title=""]')
    if not buttons:
        return 1
    return int(buttons[-1].find("span").text)

def get_pretty_price(price):
    price, _ = price.split("\n")
    price = int(price.replace(" ", ""))
    return price

def get_products(category, link, page=1, data=None):
    if data is None:
        data = []
    pagination = get_pagination(link)
    soup = get_soup(link + f"?page={page}")
    products = soup.find_all("div", class_="col-3")
    data += [
        {
            "Name": product.find("h2").text.strip(),
            "Price": get_pretty_price(product.find("div", class_="product-price__current").text.strip()),
            "Link": HOST + product.find("a").get("href"),
            "Category Name": category,
            "Category Link": link,
            "Img" : product.find("img", class_="product-image").get("data-src"),
            "characteristics": get_characteristics(HOST + product.find("a").get("href"))
        }
        for product in products
    ]
    if pagination == page:
        return data
    return get_products(category, link, page+1, data)


def get_char_link(link):
    CHAR_LINK = "https://gw.texnomart.uz/api/web/v1/product/characters?id="
    _, link = link.split("detail/")
    link, _ = link.split("/")
    return  CHAR_LINK + link


def get_characteristics(url):
    link = get_char_link(url)
    characters = {}
    response = requests.get(link)
    data = response.json()
    for d in data["data"]["data"]:
        for elem in d["characters"]:
            name = elem["name"]
            value = elem["value"]
            characters[name] = value
    return characters



def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename)

def main():
   categories = get_categories()
   data = [
       product
       for category in categories[:1]
       for product in get_products(category["title"], category["link"])[:1]
   ]
   
   save_to_excel(data, "data.xlsx")
   save_to_json(data, "data.json")


if __name__ == "__main__":
    main()