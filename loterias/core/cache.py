from typing import Annotated

from bson import ObjectId
from fastapi import Depends
from redis import StrictRedis

from ..core.settings import config
from ..enums.lottery import Lottery
from ..models import LotteryDraw


class RedisCache(StrictRedis):
    def __init__(self, **kwargs):
        super().__init__(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True, **kwargs)

    def set_cached_draw(self, lottery: Lottery, entity: LotteryDraw):
        if isinstance(entity.id, ObjectId):
            entity.id = str(entity.id)
        self.set(lottery.name, entity.model_dump_json())

    def get_cached_draw(self, lottery: Lottery):
        if entity := self.get(lottery.name):
            return LotteryDraw.model_validate_json(entity)
        return None


def get_cache():
    cache = RedisCache()
    try:
        yield cache
    finally:
        cache.close()


Cache = Annotated[RedisCache, Depends(get_cache)]
