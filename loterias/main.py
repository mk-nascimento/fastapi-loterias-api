from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()


@app.exception_handler(Exception)
def exception_handler(_: Request, exc: Exception):
    INTERNAL = HTTPStatus.INTERNAL_SERVER_ERROR
    return JSONResponse({'detail': INTERNAL.phrase}, INTERNAL)


@app.get('/', include_in_schema=False, status_code=HTTPStatus.OK)
def index():
    return HTMLResponse("Visit Swagger documentation at: <a href='/docs'>/docs</a>")
