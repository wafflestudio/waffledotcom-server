from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

from waffledotcom.src.secrets import AWSSecretManager
from waffledotcom.src.settings import settings


class DBConfig(BaseSettings):
    username: str = ""
    password: str = ""
    host: str = ""
    port: int = 0
    name: str = ""

    model_config = SettingsConfigDict(
        case_sensitive=False, env_prefix="DB_", env_file=settings.env_files
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        aws_secrets = AWSSecretManager()
        if aws_secrets.is_available():
            self.username = aws_secrets.get_secret("db_username")
            self.password = quote_plus(aws_secrets.get_secret("db_password"))
            self.host = aws_secrets.get_secret("db_host")
            self.port = int(aws_secrets.get_secret("db_port"))
            self.name = aws_secrets.get_secret("db_name")

    @property
    def url(self) -> str:
        return (
            f"mysql+mysqldb://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
            "?charset=utf8mb4"
        )


db_config = DBConfig()
