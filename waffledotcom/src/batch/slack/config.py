from pydantic_settings import BaseSettings

from waffledotcom.src.secrets import AWSSecretManager


class SlackConfig(BaseSettings):
    token: str = ""

    def __init__(self) -> None:
        super().__init__()

        aws_secret = AWSSecretManager()
        if aws_secret.is_available():
            self.token = aws_secret.get_secret("slack_token")


slack_config = SlackConfig()
