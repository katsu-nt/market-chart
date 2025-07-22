# app/services/import_vcb.py
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.exchange_rates import ExchangeRate, ExchangeRateType
from app.scrapers.vcb_exchange_rates_history import fetch_exchange_rate


def save_exchange_rates(data: dict, db):
    """Lưu 1 bản ghi exchange rate vào DB"""
    timestamp = datetime.fromisoformat(data["UpdatedDate"])
    for item in data["Data"]:
        code = item["currencyCode"]
        name = item["currencyName"]

        # Upsert loại tiền tệ
        rate_type = db.query(ExchangeRateType).filter_by(code=code).first()
        if not rate_type:
            rate_type = ExchangeRateType(code=code, name=name)
            db.add(rate_type)
            db.flush()  # Lấy id sau khi insert

        # Tạo hoặc cập nhật tỷ giá
        rate = ExchangeRate(
            timestamp=timestamp,
            type_id=rate_type.id,
            source="vcb",
            cash_rate=item.get("cash") or None,
            transfer_rate=item.get("transfer") or None,
            sell_rate=item.get("sell") or None,
        )
        db.merge(rate)


def import_vcb_range(start_date: str, end_date: str):
    db = SessionLocal()
    try:
        current = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            print(f"📥 Fetching: {date_str}")
            data = fetch_exchange_rate(date_str)
            save_exchange_rates(data, db)
            current += timedelta(days=1)
        db.commit()
        print("✅ Done importing.")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
    finally:
        db.close()


def main():
    # 🗓️ Chỉnh ngày tại đây để test
    import_vcb_range("2025-07-01", "2025-07-05")


if __name__ == "__main__":
    main()
