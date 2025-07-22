from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, date
from app.database import get_db
from app.models.exchange_rates import DailyExchangeRate, ExchangeRate

router = APIRouter(prefix="/exchange-rates", tags=["Exchange Rates"])


def wrap_response(data: list, status_code: int = 200, message: str = "success"):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "data": data
        }
    )


@router.get("/live")
def get_current_exchange_rates(db: Session = Depends(get_db)):
    results = db.query(DailyExchangeRate).options(
        joinedload(DailyExchangeRate.rate_type)
    ).all()

    if not results:
        return wrap_response([], status_code=404, message="Không có dữ liệu hôm nay")

    return wrap_response([r.as_dict() for r in results])


@router.get("/by-date")
def get_exchange_rates_by_date(
    date: date = Query(..., description="Ngày cần truy xuất (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    start_dt = datetime.combine(date, datetime.min.time())
    end_dt = datetime.combine(date, datetime.max.time())

    results = db.query(ExchangeRate).options(
        joinedload(ExchangeRate.rate_type)
    ).filter(ExchangeRate.timestamp.between(start_dt, end_dt)).all()

    if not results:
        return wrap_response([], status_code=404, message="Không có dữ liệu cho ngày đã chọn")

    return wrap_response([r.as_dict() for r in results])


@router.get("/range")
def get_exchange_rates_in_range(
    start: date = Query(...),
    end: date = Query(...),
    db: Session = Depends(get_db)
):
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.max.time())

    results = db.query(ExchangeRate).options(
        joinedload(ExchangeRate.rate_type)
    ).filter(ExchangeRate.timestamp.between(start_dt, end_dt)).all()

    if not results:
        return wrap_response([], status_code=404, message="Không có dữ liệu trong khoảng thời gian đã chọn")

    return wrap_response([r.as_dict() for r in results])
