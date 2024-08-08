import logging
from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, IndexModel

from ..enums.lottery import Lottery
from .settings import config

logger = logging.getLogger(__name__)


class LotteryDatabase:
    db: AsyncIOMotorDatabase
    client: AsyncIOMotorClient

    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name

    async def startup(self):
        try:
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client.get_database(self.db_name)

            await self.__create_indexes()

            logger.info('Database connection established.')
        except Exception as e:
            logger.exception(e)

    def shutdown(self):
        if self.client:
            self.client.close()
            logger.info('Database connection finished')
        else:
            logger.warning('No database connection to close.')

    async def __create_indexes(self):
        for enum in Lottery:
            index = ('concurso', ASCENDING)
            index_kwargs = dict(name='_concurso', unique=True)
            await self.db[enum.value].create_indexes([IndexModel([index], **index_kwargs)])


Database = LotteryDatabase(config.MONGO_URI.unicode_string(), config.MONGODB_DB)


async def get_db():
    try:
        await Database.startup()
        yield Database
    finally:
        Database.shutdown()


Session = Annotated[LotteryDatabase, Depends(get_db)]
