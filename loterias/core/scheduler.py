import logging
from asyncio import sleep
from calendar import SUNDAY
from datetime import datetime

from aiohttp import ClientSession
from aiohttp.web_exceptions import HTTPSuccessful
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tenacity import retry, stop_after_attempt, wait_fixed
from tenacity import retry_if_not_exception_type as retry_if_not

from ..constants import BRAZILIAN_TIMEZONE, MIN_IN_HOUR, SEC_IN_MINUTE
from ..enums.lottery import Lottery
from ..models import LotteryDraw
from .settings import config

DAILY_JITTER, YEARLY_JITTER = ((SEC_IN_MINUTE * 10), (SEC_IN_MINUTE * MIN_IN_HOUR))

scd = AsyncIOScheduler(timezone=BRAZILIAN_TIMEZONE)
logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(SEC_IN_MINUTE / 6), retry=retry_if_not(HTTPSuccessful))
async def __fetch_latest_lottery_draw(lottery: Lottery):
    try:
        async with ClientSession(f'{config.EXTERNAL_API}') as client:
            res = await client.get(f'/{config.EXTERNAL_API_ENDPOINT}/{lottery.value}', raise_for_status=True)
            if instance := LotteryDraw.model_validate_json(await res.text()):
                async with ClientSession('http://localhost:8000') as internal:
                    headers = {'x-internal-token': config.SECRET_TOKEN}
                    json = instance.model_dump(mode='json', by_alias=True)

                    await internal.post('/admin/fetch', headers=headers, json=json)
                    logger.info(f'`{lottery.name}` updated')
    except Exception as exc:
        logger.exception(exc)
        raise exc


@scd.scheduled_job('cron', day_of_week='mon-sat', hour=20, minute=30, jitter=DAILY_JITTER)
async def load_lottery_draw():
    for enum in Lottery:
        await __fetch_latest_lottery_draw(enum)
        await sleep(5)


@scd.scheduled_job('cron', month=12, day=31, hour=20, minute=30, jitter=YEARLY_JITTER)
async def reveillon_lottery_draw():
    now = datetime.now(BRAZILIAN_TIMEZONE)
    if now.weekday() == SUNDAY:
        await __fetch_latest_lottery_draw(Lottery.MEGA_SENA)


def scheduler_startup():
    scd.start()
    scd.print_jobs()


def scheduler_shutdown():
    scd.remove_all_jobs()
    scd.shutdown()
