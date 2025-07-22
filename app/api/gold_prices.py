from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, date
from app.database import get_db
from app.models import DailyGoldPrice, GoldPrice

router = APIRouter(prefix="/gold-prices", tags=["Gold Prices"])


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
def get_current_gold_prices(db: Session = Depends(get_db)):
    results = db.query(DailyGoldPrice).options(
        joinedload(DailyGoldPrice.gold_type),
        joinedload(DailyGoldPrice.unit)
    ).all()

    if not results:
        return wrap_response([], status_code=404, message="Không có dữ liệu live")
    
    return wrap_response([r.as_dict() for r in results])


@router.get("/by-date")
def get_gold_prices_by_date(
    date: date = Query(..., description="Ngày cần truy xuất (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    start_dt = datetime.combine(date, datetime.min.time())
    end_dt = datetime.combine(date, datetime.max.time())

    results = db.query(GoldPrice).options(
        joinedload(GoldPrice.gold_type),
        joinedload(GoldPrice.unit)
    ).filter(GoldPrice.timestamp.between(start_dt, end_dt)).all()

    if not results:
        return wrap_response([], status_code=404, message="Không có dữ liệu cho ngày đã chọn")

    return wrap_response([r.as_dict() for r in results])


@router.get("/range")
def get_gold_prices_in_range(
    start: date = Query(...),
    end: date = Query(...),
    db: Session = Depends(get_db)
):
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.max.time())

    results = db.query(GoldPrice).options(
        joinedload(GoldPrice.gold_type),
        joinedload(GoldPrice.unit)
    ).filter(GoldPrice.timestamp.between(start_dt, end_dt)).all()

    if not results:
        return wrap_response([], status_code=404, message="Không có dữ liệu trong khoảng thời gian đã chọn")

    return wrap_response([r.as_dict() for r in results])
