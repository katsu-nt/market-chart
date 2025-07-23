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

    value = Column(Numeric(20, 6))

    __table_args__ = (
        PrimaryKeyConstraint("timestamp", "type_id", "source"),
        Index("ix_exchange_rates_type_time", "type_id", "timestamp"),
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
            "value": float(self.value) if self.value is not None else None,
        }






