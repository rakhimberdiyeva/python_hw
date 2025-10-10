import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.gazeta.uz/ru/"
HOST = "https://www.gazeta.uz/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

def get_soup(link):
    request = requests.get(link, headers=headers)
    html = request.text
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_category():
    data = []
    soup = get_soup(URL)
    cont = soup.find("ul", class_="head-container-items")
    items = cont.find_all("li")
    for i in items:
        name = i.find("a").text
        link = HOST + i.find("a").get("href")
        data.append(
            {
                "category": name,
                "link": link
            }
        )

    cont2 = soup.find("ul", class_="nav__container-items")
    items2 = cont2.find_all("li")
    for i in items2[:-1]:
        name2 = i.find("a").text
        link2 = HOST + i.find("a").get("href")
        data.append(
            {
                "category": name2,
                "link": link2
            }
        )

    return data

def get_article(url):
    articles = []
    soup = get_soup(url)
    news_block = soup.find("div", class_="newsblock-2")
    news = news_block.find_all("div", class_="nblock")
    for n in news:
        title = n.find("h3").find("a").text
        description = n.find("p").text
        time = n.find("div", class_="ndt").text
        img = n.find("img", class_="lazy").get("data-src")
        link = HOST + n.find("h3").find("a").get("href")
        articles.append(
            {
                "title": clean_text(title),
                "description": clean_text(description),
                "time": clean_text(description),
                "img": img,
                "link": link
            }
        )
    return articles

def clean_text(text):
    new_text = text.replace("\xa0", " ")
    return new_text


def main():
    data = get_category()
    for category in data:
        articles = get_article(category["link"])
        category["articles"] = articles
    with open("data.json", "w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ ==  "__main__":
    main()




