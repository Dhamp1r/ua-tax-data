import json
import re
import requests
from bs4 import BeautifulSoup

URL = "https://index.minfin.com.ua/ua/economy/index/inflation/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_inflation():
    res = requests.get(URL, headers=HEADERS, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.find("table")
    if not table:
        print("Таблицю не знайдено")
        return {}

    result = {}
    rows = table.find_all("tr")

    for row in rows:
        cols = [td.get_text(strip=True).replace(",", ".") for td in row.find_all(["td", "th"])]
        if not cols:
            continue

        year_match = re.match(r"^(\d{4})$", cols[0])
        if year_match:
            year = int(year_match.group(1))
            result[year] = {}
            for month_idx in range(1, 13):
                if month_idx < len(cols):
                    val_str = cols[month_idx]
                    try:
                        val = float(val_str)
                        if val > 50.0:
                            result[year][month_idx] = val
                    except ValueError:
                        pass

    return result

if __name__ == "__main__":
    data = fetch_inflation()
    if data:
        with open("inflation.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("inflation.json успішно оновлено!")
