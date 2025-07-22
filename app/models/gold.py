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
from pytz import timezone

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

    timestamp = Column(TIMESTAMP(timezone=True), primary_key=True)
    unit_id = Column(Integer, ForeignKey("units.id"), primary_key=True)
    location = Column(String(100), primary_key=True)
    gold_type_id = Column(Integer, ForeignKey("gold_types.id"), primary_key=True)

    buy_price = Column(DECIMAL(15, 2), nullable=False)
    sell_price = Column(DECIMAL(15, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    gold_type = relationship("GoldType", back_populates="prices")
    unit = relationship("Unit", back_populates="prices")

    def as_dict(self):
        tz = timezone("Asia/Ho_Chi_Minh")
        localized_ts = self.timestamp.astimezone(tz)  # chuyển sang giờ Việt Nam
        return {
            "timestamp": localized_ts.isoformat(),
            "buy_price": float(self.buy_price),
            "sell_price": float(self.sell_price),
            "location": self.location,
            "gold_type": self.gold_type.name if self.gold_type else None,
            "gold_type_description": self.gold_type.description if self.gold_type else None,
            "unit": self.unit.name if self.unit else None,
            "unit_description": self.unit.description if self.unit else None,
        }



class DailyGoldPrice(Base):
    __tablename__ = "daily_gold_prices"

    timestamp = Column(TIMESTAMP(timezone=True), primary_key=True)
    unit_id = Column(Integer, ForeignKey("units.id"), primary_key=True)
    location = Column(String(100), primary_key=True)
    gold_type_id = Column(Integer, ForeignKey("gold_types.id"), primary_key=True)

    buy_price = Column(DECIMAL(15, 2), nullable=False)
    sell_price = Column(DECIMAL(15, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    gold_type = relationship("GoldType", back_populates="daily_prices")
    unit = relationship("Unit", back_populates="daily_prices")

    def as_dict(self):
        tz = timezone("Asia/Ho_Chi_Minh")
        localized_ts = self.timestamp.astimezone(tz)  # chuyển sang giờ Việt Nam
        return {
            "timestamp": localized_ts.isoformat(),
            "buy_price": float(self.buy_price),
            "sell_price": float(self.sell_price),
            "location": self.location,
            "gold_type": self.gold_type.name if self.gold_type else None,
            "gold_type_description": self.gold_type.description if self.gold_type else None,
            "unit": self.unit.name if self.unit else None,
            "unit_description": self.unit.description if self.unit else None,
        }
