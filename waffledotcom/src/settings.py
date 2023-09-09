from pathlib import Path
from typing import Literal

from pydantic import BaseSettings

ROOT_PATH = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    env: Literal["dev", "prod", "local"] = "local"

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
    def env_files(self) -> tuple[Path, ...]:
        if self.is_local:
            return (ROOT_PATH / ".env.local",)

        return (
            ROOT_PATH / f".env.{self.env}",
            ROOT_PATH / f".env.{self.env}.local",
        )


settings = Settings()
