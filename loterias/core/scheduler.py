from calendar import SUNDAY
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..constants import BRAZILIAN_TIMEZONE
from ..core.cache import get_cache
from ..core.database import get_db
from ..enums.lottery import Lottery
from ..models import LotteryDraw
from .services import cache_lottery_draw, fetch_external_data, save_lottery_draw

scd = AsyncIOScheduler(timezone=BRAZILIAN_TIMEZONE)


@scd.scheduled_job('cron', day_of_week='mon-sat', hour=21)
async def daily_fetch_lottery_draw():
    for enum in Lottery:
        res = await fetch_external_data(enum=enum)
        model = LotteryDraw.model_validate(res)

        async for mongo in get_db():
            await save_lottery_draw(db=mongo.db, model=model)
        for cache in get_cache():
            await cache_lottery_draw(cache=cache, model=model)


@scd.scheduled_job('cron', month=12, day=31, hour=21)
async def reveillon_fetch_lottery_draw():
    now = datetime.now(BRAZILIAN_TIMEZONE)
    if now.weekday() == SUNDAY:
        res = await fetch_external_data(enum=Lottery.MEGA_SENA)
        model = LotteryDraw.model_validate(res)

        async for mongo in get_db():
            await save_lottery_draw(db=mongo.db, model=model)
        async for cache in get_cache():
            await cache_lottery_draw(cache=cache, model=model)


def scheduler_startup():
    scd.start()
    scd.print_jobs()


def scheduler_shutdown():
    scd.remove_all_jobs()
    scd.shutdown()
