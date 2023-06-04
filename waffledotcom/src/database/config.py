from pydantic import BaseSettings

from waffledotcom.src.settings import ROOT_PATH
from waffledotcom.src.settings import Settings


class DBConfig(BaseSettings):
    username: str = ""
    password: str = ""
    host: str = ""
    port: int = 0
    name: str = ""

    class Config:
        case_sensitive = False
        env_prefix = "DB_"

        site = Settings().env
        env_file = (
            (
                ROOT_PATH / f".env.{site}",
                ROOT_PATH / f".env.{site}.local",
            )
            if site != "local"
            else ROOT_PATH / ".env.local"
        )

    @property
    def url(self) -> str:
        return (
            f"mysql+mysqldb://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )
