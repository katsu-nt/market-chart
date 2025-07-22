from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, DECIMAL, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ExchangeRateType(Base):
    __tablename__ = "exchange_rate_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    source = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("name", "source", name="unique_exchange_rate_type"),
    )

    rates = relationship("ExchangeRate", back_populates="rate_type")


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    rate_type_id = Column(Integer, ForeignKey("exchange_rate_types.id"), nullable=False)
    buy_rate = Column(DECIMAL(15, 4), nullable=True)
    sell_rate = Column(DECIMAL(15, 4), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("timestamp", "rate_type_id", name="unique_exchange_rate_entry"),
    )

    rate_type = relationship("ExchangeRateType", back_populates="rates")
