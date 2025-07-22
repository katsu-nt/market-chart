import asyncio
from app.scrapers.investing_live import fetch_xau_usd_and_usd_vnd
from app.models import DailyGoldPrice, GoldType, Unit
from app.database import SessionLocal
from app.db.utils import get_or_create
from datetime import datetime
import pytz


def normalize_unit():
    return "tael", "1000VND/Lượng"


async def import_xau_vnd_live():
    print("📡 Fetching XAU/USD & USD/VND...")
    db = SessionLocal()
    try:
        # ⚙️ Gọi hàm sync trong thread async
        prices = await asyncio.to_thread(fetch_xau_usd_and_usd_vnd)
        xau_usd = prices["xau_usd"]
        usd_vnd = prices["usd_vnd"]

        # 💰 Tính giá theo VNĐ/lượng
        xau_vnd_per_tael = round((xau_usd * usd_vnd) / 0.829 / 1000, 2)
        print(f"💰 XAU/VND per tael: {xau_vnd_per_tael:,.2f}")

        gold_type = get_or_create(
            db,
            GoldType,
            {"name": "xau_vnd"},
            {"description": "Giá vàng thế giới"},
        )
        unit_name, unit_desc = normalize_unit()
        unit = get_or_create(
            db,
            Unit,
            {"name": unit_name},
            {"description": unit_desc},
        )

        # 🧹 Xoá tất cả các bản ghi xau_vnd cũ trong hôm nay
        now = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
        deleted = db.query(DailyGoldPrice).filter(
            DailyGoldPrice.gold_type_id == gold_type.id,
            DailyGoldPrice.unit_id == unit.id,
            DailyGoldPrice.location == "global",
        ).delete(synchronize_session=False)
        print(f"🧹 Deleted {deleted} old xau_vnd records")

        # ✅ Thêm bản ghi mới
        timestamp = now.replace(minute=0, second=0, microsecond=0)
        db.add(DailyGoldPrice(
            timestamp=timestamp,
            gold_type_id=gold_type.id,
            unit_id=unit.id,
            location="global",
            buy_price=0,
            sell_price=xau_vnd_per_tael,
        ))

        db.commit()
        print("✅ Inserted new xau_vnd daily record")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
    finally:
        db.close()


# Dùng cho chạy tay: python app/services/import_xau_vnd_live.py
if __name__ == "__main__":
    asyncio.run(import_xau_vnd_live())
