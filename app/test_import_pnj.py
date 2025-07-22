import asyncio
from datetime import datetime
from app.services.pnj_importer import import_pnj_range

if __name__ == "__main__":
    start = datetime(2021, 1, 1)
    end = datetime(2021, 12, 31)
    asyncio.run(import_pnj_range(start, end))
