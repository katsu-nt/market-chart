from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    DECIMAL,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class GoldType(Base):
    __tablename__ = "gold_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    source = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("name", "source", name="unique_gold_type_per_source"),
    )

    prices = relationship("GoldPrice", back_populates="gold_type")
    daily_prices = relationship("DailyGoldPrice", back_populates="gold_type")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    prices = relationship("GoldPrice", back_populates="unit")
    daily_prices = relationship("DailyGoldPrice", back_populates="unit")


class GoldPrice(Base):
    __tablename__ = "gold_prices"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    gold_type_id = Column(Integer, ForeignKey("gold_types.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    buy_price = Column(DECIMAL(15, 2), nullable=False)
    sell_price = Column(DECIMAL(15, 2), nullable=False)
    location = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "timestamp", "unit_id", "location", "gold_type_id", name="unique_gold_entry"
        ),
    )
    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "buy_price": float(self.buy_price),
            "sell_price": float(self.sell_price),
            "location": self.location,
            "gold_type": self.gold_type.name if self.gold_type else None,
            "unit": self.unit.name if self.unit else None,
        }


    gold_type = relationship("GoldType", back_populates="prices")
    unit = relationship("Unit", back_populates="prices")


class DailyGoldPrice(Base):
    __tablename__ = "daily_gold_prices"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    gold_type_id = Column(Integer, ForeignKey("gold_types.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    buy_price = Column(DECIMAL(15, 2), nullable=False)
    sell_price = Column(DECIMAL(15, 2), nullable=False)
    location = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "timestamp", "unit_id", "location", "gold_type_id", name="unique_gold_daily_entry"
        ),
    )
    def as_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "buy_price": float(self.buy_price),
            "sell_price": float(self.sell_price),
            "location": self.location,
            "gold_type": self.gold_type.name if self.gold_type else None,
            "unit": self.unit.name if self.unit else None,
        }


    gold_type = relationship("GoldType", back_populates="daily_prices")
    unit = relationship("Unit", back_populates="daily_prices")
