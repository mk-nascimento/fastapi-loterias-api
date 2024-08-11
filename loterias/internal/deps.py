from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, Header, HTTPException

from ..core.settings import config


async def verify_access_token(x_internal_token: Annotated[str, Header()]):
    if x_internal_token != config.SECRET_TOKEN:
        raise HTTPException(HTTPStatus.BAD_REQUEST, x_internal_token)


AdminDeps = [Depends(verify_access_token)]
