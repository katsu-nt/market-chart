import pandas as pd
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.exchange_rates import ExchangeRate, ExchangeRateType
from app.models.exchange_index import ExchangeIndex, ExchangeIndexType


def clean_value(val):
    """Loại bỏ dấu ',' và ép sang float. Trả về None nếu không hợp lệ."""
    if pd.isna(val):
        return None
    try:
        return float(str(val).replace(",", "").strip())
    except ValueError:
        return None


def import_usd_vnd(file_path: str, source: str = "bloomberg"):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["value"])

    db = SessionLocal()
    try:
        # Tìm hoặc tạo loại tỷ giá USD
        code = "USD"
        rate_type = db.query(ExchangeRateType).filter_by(code=code).first()
        if not rate_type:
            rate_type = ExchangeRateType(code=code, name="US Dollar")
            db.add(rate_type)
            db.flush()

        for _, row in df.iterrows():
            timestamp = datetime.strptime(row["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            value = clean_value(row["value"])
            if value is None:
                continue

            rate = ExchangeRate(
                timestamp=timestamp,
                type_id=rate_type.id,
                source=source,
                value=value,
            )
            db.merge(rate)

        db.commit()
        print("✅ Imported USD/VND exchange rates")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
    finally:
        db.close()


def import_dxy(file_path: str, source: str = "bloomberg"):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["value"])

    db = SessionLocal()
    try:
        # Tìm hoặc tạo loại chỉ số DXY
        code = "DXY"
        index_type = db.query(ExchangeIndexType).filter_by(code=code).first()
        if not index_type:
            index_type = ExchangeIndexType(code=code, name="US Dollar Index (DXY)")
            db.add(index_type)
            db.flush()

        for _, row in df.iterrows():
            date = datetime.strptime(row["date"], "%Y-%m-%d").date()
            value = clean_value(row["value"])
            if value is None:
                continue

            index = ExchangeIndex(
                date=date,
                type_id=index_type.id,
                value=value,
                source=source,
            )
            db.merge(index)

        db.commit()
        print("✅ Imported DXY index data")
    except Exception as e:
        db.rollback()
        print("❌ Error:", e)
    finally:
        db.close()


def main():
    import_usd_vnd("app/scrapers/csv-data/Bloomberg_data_1990-2025_cleaned_vnd.csv")
    import_dxy("app/scrapers/csv-data/Bloomberg_data_1990-2025_cleaned_dxy.csv")


if __name__ == "__main__":
    main()
