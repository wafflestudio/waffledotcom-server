from pydantic import BaseSettings

from waffledotcom.src.settings import ROOT_PATH
from waffledotcom.src.settings import Settings


class DBConfig(BaseSettings):
    username: str = ""
    password: str = ""
    host: str = ""
    port: int = 0
    db_name: str = ""

    class Config:
        case_sensitive = False
        env_prefix = "DATABASE_"

        dev_or_prod = Settings().env
        env_file = (
            ROOT_PATH / f".env.{dev_or_prod}",
            ROOT_PATH / f".env.{dev_or_prod}.local",
        )

    @property
    def url(self) -> str:
        return f"mysql+mysqldb://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
