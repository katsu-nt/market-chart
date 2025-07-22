from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import asyncio
from app.services.import_pnj_daily import import_pnj_daily
from app.services.import_xau_vnd_live import import_xau_vnd_live
from app.services.transfer_to_gold_prices import transfer_daily_to_gold_prices

scheduler = BackgroundScheduler(timezone=timezone("Asia/Ho_Chi_Minh"))


def start():
    scheduler.add_job(
        lambda: asyncio.run(import_pnj_daily()),
        CronTrigger(minute=1, second=15),
        id="hourly_scraper",
        replace_existing=True,
    )
    scheduler.add_job(
        lambda: asyncio.run(import_xau_vnd_live()),
        CronTrigger(minute=1, second=45),
        id="hourly_xau_vnd",
        replace_existing=True,
    )
    scheduler.add_job(
        lambda: asyncio.run(transfer_daily_to_gold_prices()),
        CronTrigger(hour=23, minute=57),
        id="daily_eod",
        replace_existing=True,
    )
    scheduler.start()


## Test script
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# from pytz import timezone
# import asyncio
# from app.services.import_pnj_daily import import_pnj_daily
# from app.services.import_xau_vnd_live import import_xau_vnd_live
# from app.services.transfer_to_gold_prices import transfer_daily_to_gold_prices

# scheduler = BackgroundScheduler(timezone=timezone("Asia/Ho_Chi_Minh"))

# def start():
#     # ⏱ Every minute (for testing only)
#     scheduler.add_job(
#         lambda: asyncio.run(import_pnj_daily()),
#         CronTrigger(minute="*/1"),  # Run every minute
#         id="test_hourly_scraper",
#         replace_existing=True,
#     )
#     scheduler.add_job(
#         lambda: asyncio.run(import_xau_vnd_live()),
#         CronTrigger(minute="*/1"),
#         id="hourly_xau_vnd",
#         replace_existing=True,
#     )

#     # ⏱ Every 2 minutes (for testing only)
#     scheduler.add_job(
#         lambda: asyncio.run(transfer_daily_to_gold_prices()),
#         CronTrigger(minute="*/2"),  # Run every 2 minutes
#         id="test_daily_eod",
#         replace_existing=True,
#     )

#     scheduler.start()
