from app.scrapers.pnj_live import fetch_pnj_live
from app.models import DailyGoldPrice, GoldType, Unit
from app.database import SessionLocal
from app.db.utils import get_or_create
from datetime import datetime
import pytz


def normalize_gold_type(name: str) -> str:
    name = name.strip().lower()
    mapping = {
        "sjc": "sjc",
        "pnj": "pnj",
        "nhẫn trơn pnj 999.9": "nhan_tron_pnj_999_9",
        "vàng nữ trang 999.9": "vang_nu_trang_999_9",
        "vàng nữ trang 99": "vang_nu_trang_99",
        "vàng 750 (18k)": "vang_750_18k",
        "vàng 585 (14k)": "vang_585_14k",
        "vàng 416 (10k)": "vang_416_10k",
        "vàng 916 (22k)": "vang_916_22k",
        "vàng 650 (15.6k)": "vang_650_15_6k",
        "vàng 680 (16.3k)": "vang_680_16_3k",
        "vàng 375 (9k)": "vang_375_9k",
        "vàng 333 (8k)": "vang_333_8k",
    }
    return mapping.get(name, name.replace(" ", "_").lower())


def normalize_unit():
    return "tael", "1 Lượng"


async def import_pnj_daily():
    print("📡 Fetching PNJ live daily data...")
    db = SessionLocal()
    try:
        data = await fetch_pnj_live()
        if not data:
            return

        deleted = db.query(DailyGoldPrice).delete()
        print(f"🧹 Deleted {deleted} daily_gold_prices")

        unit_name, unit_desc = normalize_unit()
        unit = get_or_create(db, Unit, {"name": unit_name}, {"description": unit_desc})

        for rec in data:
            gold_type_code = normalize_gold_type(rec["gold_type"])
            gold_type = get_or_create(
                db,
                GoldType,
                {"name": gold_type_code, "source": "pnj"},
                {"description": rec["gold_type"]},
            )
            db.add(DailyGoldPrice(
                timestamp=rec["timestamp"],
                buy_price=rec["buy_price"],
                sell_price=rec["sell_price"],
                location=rec["location"],
                gold_type_id=gold_type.id,
                unit_id=unit.id,
            ))

        db.commit()
        print(f"✅ Inserted {len(data)} daily records")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
    finally:
        db.close()