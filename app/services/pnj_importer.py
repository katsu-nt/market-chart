import asyncio
from datetime import datetime, timedelta
from sqlalchemy import and_
from pytz import timezone

from app.scrapers.pnj_history import fetch_pnj_history
from app.database import SessionLocal
from app.models import GoldType, Unit, GoldPrice
from app.db.utils import get_or_create


def normalize_gold_type(name: str) -> str:
    name = name.strip().lower()

    mapping = {
        "sjc": "sjc",
        "pnj": "pnj",
        "nhẫn trơn pnj 999.9": "nhan_tron_pnj_999_9",
        "vàng kim bảo 999.9": "vang_kim_bao_999_9",
        "vàng phúc lộc tài 999.9": "vang_phuc_loc_tai_999_9",
        "vàng nữ trang 999.9": "vang_nu_trang_999_9",
        "vàng nữ trang 99": "vang_nu_trang_99",
        "vàng 750 (18k)": "vang_750_18k",
        "vàng 585 (14k)": "vang_585_14k",
        "vàng 416 (10k)": "vang_416_10k",
        "vàng 916 (22k)": "vang_916_22k",
        "vàng 610 (14.6k)": "vang_610_14_6k",
        "vàng 650 (15.6k)": "vang_650_15_6k",
        "vàng 680 (16.3k)": "vang_680_16_3k",
        "vàng 375 (9k)": "vang_375_9k",
        "vàng 333 (8k)": "vang_333_8k",
    }

    return mapping.get(name, name.replace(" ", "_"))  # fallback giữ unique


def normalize_unit():
    return "tael", "1 Lượng"


def normalize_location(text: str):
    return text.strip().lower()


async def import_pnj_range(start_date: datetime, end_date: datetime):
    db = SessionLocal()
    tz = timezone("Asia/Ho_Chi_Minh")

    try:
        # Ensure unit exists
        unit_name, unit_desc = normalize_unit()
        unit = get_or_create(db, Unit, {"name": unit_name}, {"description": unit_desc})

        current = start_date
        while current <= end_date:
            print(f"📆 Scraping {current.strftime('%Y-%m-%d')}")
            day, month, year = current.day, current.month, current.year
            records = await fetch_pnj_history(day, month, year)

            insert_count = 0

            for rec in records:
                location = normalize_location(rec["location"])
                gold_type_code = normalize_gold_type(rec["gold_type"])
                timestamp = rec["timestamp"]

                if timestamp is None:
                    continue  # skip rows without timestamp

                # Gắn timezone Asia/Ho_Chi_Minh nếu timestamp chưa có tzinfo
                if timestamp.tzinfo is None:
                    timestamp = tz.localize(timestamp)

                gold_type = get_or_create(
                    db,
                    GoldType,
                    {"name": gold_type_code, "source": "pnj"},
                    {"description": rec["gold_type"]}
                )

                exists = db.query(GoldPrice).filter(
                    and_(
                        GoldPrice.timestamp == timestamp,
                        GoldPrice.unit_id == unit.id,
                        GoldPrice.location == location,
                        GoldPrice.gold_type_id == gold_type.id,
                    )
                ).first()

                if exists:
                    continue

                db.add(GoldPrice(
                    timestamp=timestamp,
                    buy_price=rec["buy_price"],
                    sell_price=rec["sell_price"],
                    location=location,
                    gold_type_id=gold_type.id,
                    unit_id=unit.id,
                ))

                insert_count += 1

            db.commit()
            print(f"✅ Inserted {insert_count} new records for {current.strftime('%Y-%m-%d')}")
            current += timedelta(days=1)

    except Exception as e:
        db.rollback()
        print("❌ Error during import:", e)
    finally:
        db.close()
