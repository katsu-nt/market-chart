import httpx
from bs4 import BeautifulSoup
import pytz
from datetime import datetime
import time

URL = "https://giavang.pnj.com.vn/"


def parse_price(text):
    return float(text.replace(".", "").replace(",", "."))

tz = pytz.timezone("Asia/Ho_Chi_Minh")

def parse_timestamp(text):
    naive = datetime.strptime(text.strip(), "%d/%m/%Y %H:%M:%S")
    return tz.localize(naive)


async def fetch_pnj_live():
    for attempt in range(5):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(URL)
                response.raise_for_status()
                break
        except Exception as e:
            print(f"⚠️ Retry {attempt + 1}/5: {e}")
            time.sleep(5)
    else:
        print("❌ Failed after 5 retries")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.select(".portlet-body table")
    if not tables:
        print("⚠️ No gold price tables found")
        return []

    results = []

    for table in tables:
        rows = table.select("tbody tr")
        current_location = None

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            # Check if first column is location with rowspan
            if cols[0].has_attr("rowspan"):
                current_location = cols[0].text.strip().lower()
                cols = cols[1:]  # Remove location column

            if current_location is None:
                continue  # skip if location wasn't set before

            if len(cols) < 4:
                continue  # skip invalid rows

            gold_type = cols[0].text.strip()
            buy_price = parse_price(cols[1].text.strip())
            sell_price = parse_price(cols[2].text.strip())
            timestamp = parse_timestamp(cols[3].text.strip())

            results.append({
                "location": current_location,
                "gold_type": gold_type,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "timestamp": timestamp,
            })

    print(f"🔍 Parsed {len(results)} rows from PNJ site")
    return results
