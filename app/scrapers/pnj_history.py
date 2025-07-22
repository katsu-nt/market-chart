import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import time
from collections import defaultdict

BASE_URL = "https://giavang.pnj.com.vn/history"


def parse_price(text):
    try:
        return float(text.replace(".", "").replace(",", "."))
    except:
        return None


def parse_timestamp(text):
    try:
        return datetime.strptime(text, "%d/%m/%Y %H:%M:%S")
    except:
        return None


def get_latest_entries(entries: list[dict]) -> list[dict]:
    """
    Giữ lại bản ghi có timestamp lớn nhất cho mỗi (gold_type, location)
    """
    latest = {}
    for entry in entries:
        key = (entry["gold_type"], entry["location"])
        if key not in latest or entry["timestamp"] > latest[key]["timestamp"]:
            latest[key] = entry
    return list(latest.values())


async def fetch_pnj_history(day: int, month: int, year: int) -> list[dict]:
    """
    Scrape historical gold price data from PNJ for the given date.
    Chỉ lấy bản ghi cuối cùng trong ngày cho mỗi loại vàng + khu vực.
    """
    params = {
        "gold_history_day": str(day).zfill(2),
        "gold_history_month": str(month).zfill(2),
        "gold_history_year": str(year),
    }

    response = None
    for attempt in range(5):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(BASE_URL, params=params)
                response.raise_for_status()
                break
        except Exception as e:
            print(f"❌ Attempt {attempt + 1}/5 failed: {e}")
            if attempt < 4:
                time.sleep(5)
            else:
                print("🚫 All retry attempts failed.")
                return []

    soup = BeautifulSoup(response.text, "html.parser")
    all_tables = soup.select("div.portlet-body table")

    if len(all_tables) <= 1:
        print("⚠️ No historical tables found.")
        return []

    historical_tables = all_tables[1:]  # skip the first table (current prices)

    raw_entries = []

    for table in historical_tables:
        header = table.select_one("thead th")
        location = header.get_text(strip=True).replace("Lịch sử giá vàng", "").strip()

        rows = table.select("tbody tr")
        current_gold_type = None

        for row in rows:
            cols = row.find_all("td")
            if not cols:
                continue

            first_cell_text = cols[0].get_text(strip=True)
            if first_cell_text == "Loại vàng":
                continue  # skip header row inside tbody

            if len(cols) == 4:
                gold_type = first_cell_text
                buy_price = parse_price(cols[1].get_text(strip=True))
                sell_price = parse_price(cols[2].get_text(strip=True))
                ts = parse_timestamp(cols[3].get_text(strip=True))
                raw_entries.append({
                    "gold_type": gold_type,
                    "location": location,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "timestamp": ts,
                })
                current_gold_type = gold_type
            elif len(cols) == 3 and current_gold_type:
                buy_price = parse_price(cols[0].get_text(strip=True))
                sell_price = parse_price(cols[1].get_text(strip=True))
                ts = parse_timestamp(cols[2].get_text(strip=True))
                raw_entries.append({
                    "gold_type": current_gold_type,
                    "location": location,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "timestamp": ts,
                })

    final_results = get_latest_entries(raw_entries)
    print(f"✅ Found {len(final_results)} entries (latest per gold_type+location)")
    return final_results
