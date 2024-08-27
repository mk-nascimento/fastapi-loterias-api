import logging
from http import HTTPStatus as status

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .constants import LOGGING_FORMAT
from .core import scheduler
from .core.cache import Cache
from .core.database import Session
from .enums.lottery import Lottery
from .models import LotteryDraw

logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)


app = FastAPI()
app.add_event_handler('startup', scheduler.scheduler_startup)
app.add_event_handler('shutdown', scheduler.scheduler_shutdown)


@app.exception_handler(Exception)
def exception_handler(_: Request, exc: Exception):
    INTERNAL = status.INTERNAL_SERVER_ERROR
    return JSONResponse({'detail': INTERNAL.phrase}, INTERNAL)


@app.get('/', include_in_schema=False, status_code=status.OK)
def index():
    return HTMLResponse("Visit Swagger documentation at: <a href='/docs'>/docs</a>")


@app.get('/{loteria:str}', response_model=LotteryDraw, status_code=status.OK, tags=['Loteria'])
async def get_latest_lottery(*, session: Session, cache: Cache, loteria: Lottery):
    if cached := cache.get_cached_draw(loteria):
        return cached.model_dump()
    elif entity := await session.db[loteria.value].find_one(sort=[('concurso', -1)]):
        return LotteryDraw.model_validate(entity).model_dump()
    raise HTTPException(status.NOT_FOUND, status.NOT_FOUND.phrase)


@app.get('/{loteria:str}/{concurso:int}', response_model=LotteryDraw, status_code=status.OK, tags=['Loteria'])
async def get_lottery(*, session: Session, cache: Cache, loteria: Lottery, concurso: int):
    if not (isinstance(concurso, int) and len(str(concurso)) == 4):  # noqa: PLR2004
        raise HTTPException(status.BAD_REQUEST, '`concurso` parameter must be a 4-digit integer.')

    if (cached := cache.get_cached_draw(loteria)) is not None:
        if concurso != cached.concurso:
            raise HTTPException(status.NOT_FOUND, {concurso: status.NOT_FOUND.phrase, 'latest': cached.concurso})
        return cached.model_dump()
    elif entity := await session.db[loteria.value].find_one(dict(concurso=concurso)):
        return LotteryDraw.model_validate(entity).model_dump()
    raise HTTPException(status.NOT_FOUND, f'#{concurso} {status.NOT_FOUND.phrase}')
