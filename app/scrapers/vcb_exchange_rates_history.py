import requests

def fetch_exchange_rate(date: str) -> dict:
    """
    Fetch exchange rate data from Vietcombank API for a given date.

    Args:
        date (str): Date in format YYYY-MM-DD

    Returns:
        dict: Parsed JSON response from API
    """
    url = f"https://www.vietcombank.com.vn/api/exchangerates?date={date}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

### Test
def main():
    test_date = "2025-07-02"
    data = fetch_exchange_rate(test_date)

    print(f"✅ Exchange rates for {test_date}:")
    print(f"Count: {data.get('Count')}")
    print(f"UpdatedDate: {data.get('UpdatedDate')}")
    for entry in data.get("Data", []):
        print(f"- {entry['currencyCode']} ({entry['currencyName']}): "
              f"Cash={entry['cash']}, Transfer={entry['transfer']}, Sell={entry['sell']}")


if __name__ == "__main__":
    main()
