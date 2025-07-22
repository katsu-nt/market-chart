from datetime import datetime
from app.database import SessionLocal
from app.models.exchange_rates import DailyExchangeRate, ExchangeRateType
from app.scrapers.vcb_exchange_rates_history import fetch_exchange_rate


async def import_vcb_daily():
    db = SessionLocal()
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"📥 Importing VCB rates for {today}")

        # Xóa dữ liệu cũ trong bảng daily
        db.query(DailyExchangeRate).delete()

        # Gọi scraper
        data = fetch_exchange_rate(today)
        timestamp = datetime.fromisoformat(data["UpdatedDate"])

        for item in data["Data"]:
            code = item["currencyCode"]
            name = item["currencyName"]

            rate_type = db.query(ExchangeRateType).filter_by(code=code).first()
            if not rate_type:
                rate_type = ExchangeRateType(code=code, name=name)
                db.add(rate_type)
                db.flush()

            rate = DailyExchangeRate(
                timestamp=timestamp,
                type_id=rate_type.id,
                source="vcb",
                cash_rate=item.get("cash") or None,
                transfer_rate=item.get("transfer") or None,
                sell_rate=item.get("sell") or None,
            )
            db.merge(rate)

        db.commit()
        print("✅ VCB daily exchange rates updated.")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
    finally:
        db.close()
