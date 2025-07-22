import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import asyncio
from app.scrapers.pnj_history import fetch_pnj_history

if __name__ == "__main__":
    data = asyncio.run(fetch_pnj_history(day=3, month=1, year=2023))
    print(f"✅ Found {len(data)} entries")
    for row in data:
        print(row)
