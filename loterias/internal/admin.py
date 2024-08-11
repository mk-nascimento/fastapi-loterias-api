from http import HTTPStatus
from os import system

from fastapi import APIRouter

from ..core.cache import Cache
from ..core.database import Session
from ..core.scheduler import scheduler_shutdown, scheduler_startup
from ..enums.lottery import Lottery
from ..models import LotteryDraw
from .deps import AdminDeps

router = APIRouter(prefix='/admin', dependencies=AdminDeps, include_in_schema=False)
router.add_event_handler('startup', lambda: system('clear'))
router.add_event_handler('startup', scheduler_startup)
router.add_event_handler('shutdown', scheduler_shutdown)


@router.post('/fetch', status_code=HTTPStatus.CREATED)
async def fetch_lottery_data(*, session: Session, cache: Cache, instance: LotteryDraw):
    lottery = Lottery[instance.tipo_jogo]
    await session.db[lottery.value].update_one(
        {'concurso': instance.concurso}, {'$set': instance.model_dump(mode='json', exclude='id')}, upsert=True
    )
    if entity := await session.db[lottery.value].find_one({'concurso': instance.concurso}):
        cache.set_cached_draw(lottery, LotteryDraw.model_validate(entity))
    else:
        cache.set_cached_draw(lottery, instance)
