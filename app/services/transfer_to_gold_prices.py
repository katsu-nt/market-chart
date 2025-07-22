from app.database import SessionLocal
from app.models import DailyGoldPrice, GoldPrice
from datetime import datetime
import pytz

async def transfer_daily_to_gold_prices():
    print("🌙 Running end-of-day gold price transfer...")
    db = SessionLocal()
    try:
        all_daily = db.query(DailyGoldPrice).all()
        timestamps = {r.timestamp for r in all_daily}

        for ts in timestamps:
            db.query(GoldPrice).filter(GoldPrice.timestamp == ts).delete()

        for rec in all_daily:
            db.add(GoldPrice(
                timestamp=rec.timestamp,
                buy_price=rec.buy_price,
                sell_price=rec.sell_price,
                location=rec.location,
                gold_type_id=rec.gold_type_id,
                unit_id=rec.unit_id,
            ))

        db.commit()
        print(f"✅ Transferred {len(all_daily)} records to gold_prices")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
    finally:
        db.close()