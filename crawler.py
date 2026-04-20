import requests
from bs4 import BeautifulSoup

def search_companies(keyword):
    url = f"https://www.google.com/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for g in soup.select(".tF2Cxc"):
        title = g.select_one("h3")
        link = g.select_one("a")

        if title and link:
            results.append({
                "company": title.text,
                "link": link["href"]
            })

    return results


if __name__ == "__main__":
    data = search_companies("công ty IT Việt Nam")

    for d in data:
        print(d)