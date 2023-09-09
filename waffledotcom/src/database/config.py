from pydantic import BaseSettings

from waffledotcom.src.settings import settings


class DBConfig(BaseSettings):
    username: str = ""
    password: str = ""
    host: str = ""
    port: int = 0
    name: str = ""

    class Config:
        case_sensitive = False
        env_prefix = "DB_"

        env_file = settings.env_files

    @property
    def url(self) -> str:
        return (
            f"mysql+mysqldb://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )
