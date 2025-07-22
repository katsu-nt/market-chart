from app.database import SessionLocal
from app.models.exchange_rates import DailyExchangeRate, ExchangeRate


async def transfer_daily_to_exchange_rates():
    db = SessionLocal()
    try:
        print("🔄 Transferring daily exchange rates to main table...")

        daily_rates = db.query(DailyExchangeRate).all()
        for row in daily_rates:
            db.merge(ExchangeRate(
                timestamp=row.timestamp,
                type_id=row.type_id,
                source=row.source,
                cash_rate=row.cash_rate,
                transfer_rate=row.transfer_rate,
                sell_rate=row.sell_rate,
            ))

        db.commit()
        print("✅ Transfer to exchange_rates complete.")
    except Exception as e:
        db.rollback()
        print("❌ Transfer error:", e)
    finally:
        db.close()
