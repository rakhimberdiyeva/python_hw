import asyncio
import httpx
import json
from bs4 import BeautifulSoup

URL = "https://sports.uz/ru"
HOST = "https://sports.uz"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/141.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://sports.uz/ru",
    "Upgrade-Insecure-Requests": "1",
}


client = httpx.AsyncClient(timeout=httpx.Timeout(30))

async def get_soup(link):
    response = await client.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

async def get_categories():
    soup = await get_soup(URL)
    data = []
    nav = soup.find_all("ul", class_="navbar-nav")[0]
    categories = nav.find_all("li", class_="nav-item")[2:8]
    for category in categories:
        if "dropdown-toggle" in category.find("a", class_="nav-link").get("class"):
            li = category.find_all("a", class_="dropdown-item")
            for item in li:
                data.append(
                    {
                        "title": item.text.strip(),
                        "link": HOST + item.get("href")
                    }
                )
            continue
        data.append(
            {
                "title": category.find("a").text.strip(),
                "link": HOST + category.find("a").get("href")
            }
        )

    return data


async def get_articles(link):
    soup = await get_soup(link)
    lst = soup.find("div", class_="news-list")
    blocks = lst.find_all("div", class_="item")
    articles = []
    for article in blocks:
        if "ads-item" in article.get("class"):
            continue
        title = article.find("h3").text.strip()
        description = article.find("p").text.strip()
        img = article.find("img", class_="lazy").get("data-src")
        link = HOST + article.find("a").get("href")
        articles.append(
            {
                "title": title,
                "description": description,
                "img": img,
                "link": link,
            }
        )
    return  articles


def to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def main():
    data = await get_categories()
    tasks = [get_articles(category["link"]) for category in data]
    res = await asyncio.gather(*tasks)

    for i in range(len(data)):
        data[i]["articles"] = res[i]

    # for category in data:
    #     articles = await get_articles(category["link"])
    #     category["articles"] = articles
    to_json("articles.json", data)


if __name__ == "__main__":
    asyncio.run(main())



