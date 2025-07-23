from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.database import SessionLocal
from app.models.exchange_rates import ExchangeRate, ExchangeRateType
from app.scrapers.vcb_exchange_rates_history import fetch_exchange_rate


def save_exchange_rates(data: dict, db):
    """Lưu nhiều bản ghi exchange rate vào DB với upsert và loại bản ghi trùng khóa trong cùng batch"""
    from datetime import datetime
    from sqlalchemy.dialects.postgresql import insert as pg_insert

    timestamp = datetime.fromisoformat(data["UpdatedDate"])
    records = []
    seen_keys = set()

    for item in data["Data"]:
        code = item["currencyCode"]
        name = item["currencyName"]

        # Upsert loại tiền tệ nếu chưa có
        rate_type = db.query(ExchangeRateType).filter_by(code=code).first()
        if not rate_type:
            rate_type = ExchangeRateType(code=code, name=name)
            db.add(rate_type)
            db.flush()

        key = (timestamp, rate_type.id, "vcb")
        if key in seen_keys:
            continue  # loại bỏ bản ghi trùng trong batch
        seen_keys.add(key)

        records.append({
            "timestamp": timestamp,
            "type_id": rate_type.id,
            "source": "vcb",
            "cash_rate": item.get("cash") or None,
            "transfer_rate": item.get("transfer") or None,
            "sell_rate": item.get("sell") or None,
        })

    if records:
        stmt = pg_insert(ExchangeRate).values(records)
        stmt = stmt.on_conflict_do_update(
            index_elements=["timestamp", "type_id", "source"],
            set_={
                "cash_rate": stmt.excluded.cash_rate,
                "transfer_rate": stmt.excluded.transfer_rate,
                "sell_rate": stmt.excluded.sell_rate,
            }
        )
        db.execute(stmt)



def import_vcb_range(start_date: str, end_date: str):
    """Import tỷ giá từ Vietcombank trong khoảng thời gian"""
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
    # 🗓️ Chỉnh khoảng thời gian để test ở đây
    import_vcb_range("2025-01-01", "2025-07-22")


if __name__ == "__main__":
    main()
