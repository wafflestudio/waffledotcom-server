from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings

ROOT_PATH = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    env: Literal["dev", "prod", "local", "test"] = "local"

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"

    @property
    def is_local(self) -> bool:
        return self.env == "local"

    @property
    def is_test(self) -> bool:
        return self.env == "test"

    @property
    def env_files(self) -> tuple[Path, ...]:
        if self.env in ["local", "test"]:
            return (ROOT_PATH / f".env.{self.env}",)

        return (
            ROOT_PATH / f".env.{self.env}",
            ROOT_PATH / f".env.{self.env}.local",
        )


settings = Settings()
