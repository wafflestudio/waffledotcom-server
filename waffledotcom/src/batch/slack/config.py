from pydantic_settings import BaseSettings, SettingsConfigDict

from waffledotcom.src.secrets import AWSSecretManager
from waffledotcom.src.settings import settings


class SlackConfig(BaseSettings):
    token: str = ""

    model_config = SettingsConfigDict(
        case_sensitive=False, env_prefix="SLACK_", env_file=settings.env_files
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        aws_secret = AWSSecretManager()
        if aws_secret.is_available():
            self.token = aws_secret.get_secret("slack_token")


slack_config = SlackConfig()
