from pathlib import Path
from typing import Literal

from pydantic import BaseSettings

ROOT_PATH = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    env: Literal["dev", "local", "prod"] = "dev"

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"

    @property
    def is_local(self) -> bool:
        return self.env == "local"

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"
