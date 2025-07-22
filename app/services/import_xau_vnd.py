import json
from pathlib import Path
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.gold import GoldPrice, GoldType, Unit
from app.db.utils import get_or_create
from datetime import datetime


def import_xau_vnd_from_json(json_path: str):
    # Mở file
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    session: Session = SessionLocal()
    try:
        # 🟢 Tạo gold_type nếu chưa có
        gold_type = get_or_create(
            session,
            GoldType,
            {"name": "xau_vnd", "source": "investing"},
            {"description": "Giá vàng thế giới"}
        )

        # 🟢 Tạo unit nếu chưa có
        unit = get_or_create(
            session,
            Unit,
            {"name": "tael"},
            {"description": "1000VND/Lượng"}
        )

        # Tạo object để insert
        gold_prices = []
        for item in data:
            gold_prices.append(GoldPrice(
                gold_type_id=gold_type.id,
                unit_id=unit.id,
                location=item["location"],
                buy_price=item["buy_price"],
                sell_price=item["sell_price"],
                timestamp=datetime.fromisoformat(item["timestamp"])
            ))

        session.bulk_save_objects(gold_prices)
        session.commit()
        print(f"✅ Đã insert {len(gold_prices)} bản ghi vào gold_prices.")
    except Exception as e:
        session.rollback()
        print("❌ Lỗi khi insert:", e)
    finally:
        session.close()


if __name__ == "__main__":
    import_xau_vnd_from_json("app/scrapers/json/xau_vnd_gold_prices.json")
