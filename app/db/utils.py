from sqlalchemy.orm import Session
from datetime import datetime
from pytz import timezone, UTC

def utc_to_local_date(dt_utc: datetime, local_tz: str = "Asia/Ho_Chi_Minh") -> datetime.date:
    """
    Convert UTC datetime to a local date (no time).
    """
    return dt_utc.replace(tzinfo=UTC).astimezone(timezone(local_tz)).date()
def get_or_create(session: Session, model, filters: dict, defaults: dict = {}):
    instance = session.query(model).filter_by(**filters).first()
    if instance:
        return instance
    params = {**filters, **defaults}
    instance = model(**params)
    session.add(instance)
    session.commit()
    return instance
