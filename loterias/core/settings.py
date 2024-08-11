from pydantic import Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..enums.settings import Environment


class LotterySettings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, extra='ignore')

    MONGODB_HOST: str = Field('localhost', alias='MONGO_INITDB_HOST')
    MONGODB_PORT: int = Field(27017, alias='MONGO_INITDB_PORT')
    MONGODB_USER: str = Field(..., alias='MONGO_INITDB_ROOT_USERNAME')
    MONGODB_PASS: str = Field(..., alias='MONGO_INITDB_ROOT_PASSWORD')
    MONGODB_DB: str = Field(..., alias='MONGO_INITDB_DATABASE')
    ENVIRONMENT: Environment = Field(Environment.DEV, alias='ENVIRONMENT')

    SECRET_TOKEN: str
    EXTERNAL_API: str
    EXTERNAL_API_ENDPOINT: str
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379

    @property
    def MONGO_URI(self) -> 'MongoDsn':
        scheme = 'mongodb'
        if self.ENVIRONMENT != Environment.PROD:
            return MongoDsn.build(
                scheme=scheme,
                host=self.MONGODB_HOST,
                port=self.MONGODB_PORT,
                username=self.MONGODB_USER,
                password=self.MONGODB_PASS,
            )
        scheme += '+srv'
        return MongoDsn.build(
            scheme=scheme, host=self.MONGODB_HOST, username=self.MONGODB_USER, password=self.MONGODB_PASS
        )


config = LotterySettings()
