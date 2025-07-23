from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    TIMESTAMP,
    ForeignKey,
    PrimaryKeyConstraint,
    Index,
    Date,
    DECIMAL
)
from sqlalchemy.orm import relationship
from app.database import Base
from pytz import timezone


class ExchangeRateType(Base):
    __tablename__ = "exchange_rate_types"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(50), nullable=True)


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    timestamp = Column(TIMESTAMP, nullable=False)
    type_id = Column(Integer, ForeignKey("exchange_rate_types.id"), nullable=False)
    source = Column(String(100), nullable=False)

    cash_rate = Column(Numeric(20, 6))
    transfer_rate = Column(Numeric(20, 6))
    sell_rate = Column(Numeric(20, 6))

    __table_args__ = (
        PrimaryKeyConstraint("timestamp", "type_id", "source"),
        # 👉 Index để tối ưu truy vấn theo loại tiền và thời gian
        Index("ix_exchange_rates_type_time", "type_id", "timestamp"),
        # 👉 Index để lọc theo thời gian nhanh
        Index("ix_exchange_rates_timestamp", "timestamp"),
    )
    rate_type = relationship("ExchangeRateType")

    def as_dict(self):
        tz = timezone("Asia/Ho_Chi_Minh")
        localized_ts = self.timestamp.astimezone(tz)
        return {
            "timestamp": localized_ts.isoformat(),
            "source": self.source,
            "currency_code": self.rate_type.code if self.rate_type else None,
            "currency_name": self.rate_type.name if self.rate_type else None,
            "cash_rate": float(self.cash_rate) if self.cash_rate else None,
            "transfer_rate": float(self.transfer_rate) if self.transfer_rate else None,
            "sell_rate": float(self.sell_rate) if self.sell_rate else None,
        }

class DailyExchangeRate(Base):
    __tablename__ = "daily_exchange_rates"

    timestamp = Column(TIMESTAMP, nullable=False)
    type_id = Column(Integer, ForeignKey("exchange_rate_types.id"), nullable=False)
    source = Column(String(100), nullable=False)

    cash_rate = Column(Numeric(20, 6))
    transfer_rate = Column(Numeric(20, 6))
    sell_rate = Column(Numeric(20, 6))

    __table_args__ = (
        PrimaryKeyConstraint("timestamp", "type_id", "source"),
        Index("ix_daily_rates_type_time", "type_id", "timestamp"),
        Index("ix_daily_rates_timestamp", "timestamp"),
    )
    rate_type = relationship("ExchangeRateType")

    def as_dict(self):
        tz = timezone("Asia/Ho_Chi_Minh")
        localized_ts = self.timestamp.astimezone(tz)
        return {
            "timestamp": localized_ts.isoformat(),
            "source": self.source,
            "currency_code": self.rate_type.code if self.rate_type else None,
            "currency_name": self.rate_type.name if self.rate_type else None,
            "cash_rate": float(self.cash_rate) if self.cash_rate else None,
            "transfer_rate": float(self.transfer_rate) if self.transfer_rate else None,
            "sell_rate": float(self.sell_rate) if self.sell_rate else None,
        }



