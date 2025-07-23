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
    # scheduler.add_job(
    #     lambda: asyncio.run(import_vcb_daily()),
    #     CronTrigger(minute=37, second=45),  # chạy vào phút thứ 10 mỗi giờ
    #     id="hourly_vcb",
    #     replace_existing=True,
    # )

    # 23h57: chuyển sang bảng chính
    # scheduler.add_job(
    #     lambda: asyncio.run(transfer_daily_to_exchange_rates()),
    #     CronTrigger(hour=23, minute=57),
    #     id="daily_vcb_eod",
    #     replace_existing=True,
    # )
    scheduler.add_job(
        lambda: asyncio.run(transfer_daily_to_gold_prices()),
        CronTrigger(hour=23, minute=57),
        id="daily_eod",
        replace_existing=True,
    )
    scheduler.start()
