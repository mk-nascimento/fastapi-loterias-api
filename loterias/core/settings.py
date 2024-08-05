from pydantic import Field, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..enums.settings import Environment


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_ignore_empty=True, extra='ignore')

    host: str = Field('localhost', alias='MONGO_INITDB_HOST')
    port: int = Field(27017, alias='MONGO_INITDB_PORT')
    user: str = Field(..., alias='MONGO_INITDB_ROOT_USERNAME')
    password: str = Field(..., alias='MONGO_INITDB_ROOT_PASSWORD')
    database: str = Field(..., alias='MONGO_INITDB_DATABASE')
    environment: Environment = Field(Environment.DEV, alias='ENVIRONMENT')

    @property
    def MONGO_URI(self) -> 'MongoDsn':
        if self.environment != Environment.PROD:
            return MongoDsn.build(
                scheme='mongodb', host=self.host, port=self.port, username=self.user, password=self.password
            )

        return MongoDsn.build(scheme='mongodb+srv', host=self.host, username=self.user, password=self.password)


Settings = Settings()
