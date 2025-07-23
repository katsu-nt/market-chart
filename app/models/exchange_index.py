from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    ForeignKey,
    Date,
    DECIMAL
)
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func 
from pytz import timezone


class ExchangeIndexType(Base):
    __tablename__ = "exchange_index_types"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)  # e.g., DXY
    name = Column(String)
    description = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

    indexes = relationship("ExchangeIndex", back_populates="type")


class ExchangeIndex(Base):
    __tablename__ = "exchange_index"

    date = Column(Date, primary_key=True)
    type_id = Column(Integer, ForeignKey("exchange_index_types.id"), primary_key=True)
    value = Column(DECIMAL(10, 4), nullable=False)
    source = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    type = relationship("ExchangeIndexType", back_populates="indexes")

    def as_dict(self):
        return {
            "date": self.date.isoformat(),
            "index_code": self.type.code if self.type else None,
            "index_name": self.type.name if self.type else None,
            "value": float(self.value),
            "source": self.source,
        }