import logging
from typing import Optional

from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorDatabase
from tenacity import retry, stop_after_delay, wait_fixed

from ..constants import MIN_IN_HOUR, SEC_IN_MINUTE
from ..enums.lottery import Lottery
from ..models import LotteryDraw
from .cache import RedisCache
from .settings import config

logger = logging.getLogger(__name__)


@retry(stop=stop_after_delay(SEC_IN_MINUTE * MIN_IN_HOUR * 2.5), wait=wait_fixed(SEC_IN_MINUTE * 15))
async def fetch_external_data(*, enum: Lottery, concurso: Optional[int] = None):
    async with ClientSession(config.EXTERNAL_API) as session:
        query = (config.EXTERNAL_API_ENDPOINT, enum.value)
        if not concurso:
            async with session.get('/%s/%s' % query, raise_for_status=True) as response:
                return await response.json()
        async with session.get('/%s/%s/%d' % (*query, concurso), raise_for_status=True) as response:
            return await response.json()


async def save_lottery_draw(*, db: AsyncIOMotorDatabase, model: LotteryDraw):
    try:
        collection = db.get_collection(Lottery[model.tipo_jogo].value)
        data = ({'concurso': model.concurso}, {'$set': model.model_dump(mode='json', exclude='id')})

        await collection.update_many({'tipo_jogo': model.tipo_jogo}, {'$set': {'ultimo_concurso': False}})
        await collection.update_one(*data, upsert=True)
    except Exception as exc:
        logger.exception(exc.__class__)
    finally:
        logger.info(('database', {model.tipo_jogo: model.concurso}))


async def cache_lottery_draw(*, cache: RedisCache, model: LotteryDraw):
    try:
        cache.set_cached_draw(Lottery[model.tipo_jogo], model)
    except Exception as exc:
        logger.exception(exc.__class__)
    finally:
        logger.info(('cached', {model.tipo_jogo: model.concurso}))
