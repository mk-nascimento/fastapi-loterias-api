import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .constants import LOGGING_FORMAT
from .core.database import Database

logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)


app = FastAPI()
app.add_event_handler('startup', Database.startup)
app.add_event_handler('shutdown', Database.shutdown)


@app.exception_handler(Exception)
def exception_handler(_: Request, exc: Exception):
    INTERNAL = HTTPStatus.INTERNAL_SERVER_ERROR
    return JSONResponse({'detail': INTERNAL.phrase}, INTERNAL)


@app.get('/', include_in_schema=False, status_code=HTTPStatus.OK)
def index():
    return HTMLResponse("Visit Swagger documentation at: <a href='/docs'>/docs</a>")
