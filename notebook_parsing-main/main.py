import json
import requests
from bs4 import BeautifulSoup

URL = "https://notebookoff.uz/catalog/"
HOST = "https://notebookoff.uz"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}

def get_soup(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_pagination(link):
    soup = get_soup(link)
    pagination = soup.find("div", class_="bx-pagination-container row")
    if pagination:
        last = pagination.select('li[class=""]')[-1].text
        return int(last)
    else:
        return 1


def get_categories():
    data = []
    soup = get_soup(URL)
    categories = soup.find_all("a", class_="bigTitle")
    for category in categories:
        title = category.text
        link = HOST + category.get("href")
        data.append(
            {
                "title": title,
                "link": link,
            }
        )
    return data

def get_products(link, page=1, data=None):
    if data is None:
        data = []
    pagination = get_pagination(link)
    soup = get_soup(link + f"/?PAGEN_1={page}")
    products = soup.find_all("div", class_="item product sku")
    for product in products:
        title = product.find("a", class_="name").text.strip()
        link = HOST + product.find("a", class_="name").get("href")
        price = product.find("a", class_="price").text.strip().replace("/ Без НДС", "").strip()
        img = HOST + product.find("a", class_="picture").find("img").get("src")
        markers = [
            marker.text.strip()
            for marker in product.find_all("div", class_="marker")
        ]
        data += [
            {
                "title": title,
                "link": link,
                "price": price.replace("\xa0", ""),
                "img": img,
                "markers": markers,
                "characteristics": get_characteristics(link)
            }
        ]
        print(data)
    if pagination == page:
        return data
    return get_products(link, page+1, data)


def get_characteristics(link):
    data = {}
    soup = get_soup(link)
    body = soup.find("table", class_="stats")
    chars = body.find_all("tr")
    for char in chars[1:]:
        name = char.find("td", class_="name").text.strip()
        value = char.find_all("td")[1].text
        data[name] = value
    return data


def get_reviews():
    data = []
    soup = get_soup("https://notebookoff.uz/reviews/")
    reviews = soup.find_all("div", class_="shop-review-item-table")
    for review in reviews:
        date = review.find("div", class_="shop-review-item-date").text.strip()
        author = review.find("div", class_="shop-review-item-author").text.strip()
        text = review.find("div", class_="shop-review-item-text").text.strip()
        data.append(
            {
                "author": author,
                "date": date,
                "text": text
            }
        )
    return data


def to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    data = get_categories()
    for category in data[:1]:
        category["products"] = get_products(category["link"])
    to_json(data, "data.json")

    # reviews = get_reviews()
    # to_json(reviews, "reviews.json")

if __name__ == "__main__":
    main()