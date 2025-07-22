import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 10


def fetch_price_from_investing(url: str) -> float:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"🌐 Fetching from {url} (attempt {attempt})")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            price_div = soup.find("div", {"data-test": "instrument-price-last"})
            if not price_div:
                raise ValueError("Không tìm thấy giá từ DOM")

            price_text = price_div.get_text().strip().replace(",", "")
            return float(price_text)
        
        except Exception as e:
            print(f"⚠️ Lỗi khi fetch {url} (attempt {attempt}): {e}")
            if attempt < MAX_RETRIES:
                print(f"⏳ Đợi {RETRY_DELAY_SECONDS} giây rồi thử lại...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                raise RuntimeError(f"❌ Fetch thất bại sau {MAX_RETRIES} lần từ {url}")


def fetch_xau_usd_and_usd_vnd() -> dict:
    xau_url = "https://vn.investing.com/currencies/xau-usd"
    vnd_url = "https://vn.investing.com/currencies/usd-vnd"

    xau_usd = fetch_price_from_investing(xau_url)
    usd_vnd = fetch_price_from_investing(vnd_url)

    return {
        "xau_usd": xau_usd,
        "usd_vnd": usd_vnd
    }


if __name__ == "__main__":
    data = fetch_xau_usd_and_usd_vnd()
    print("✅ XAU/USD:", data["xau_usd"])
    print("✅ USD/VND:", data["usd_vnd"])
