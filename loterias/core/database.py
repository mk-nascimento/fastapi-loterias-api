import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .settings import Settings

logger = logging.getLogger(__name__)


class Database:
    db: AsyncIOMotorDatabase
    client: AsyncIOMotorClient

    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name

    async def startup(self):
        try:
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client.get_database(self.db_name)

            logger.info('Database connection established.')
        except Exception as e:
            logger.exception(e)

    def shutdown(self):
        if self.client:
            self.client.close()
            logger.info('Database connection finished')
        else:
            logger.warning('No database connection to close.')


Database = Database(Settings.MONGO_URI.unicode_string(), Settings.database)
