from typing import Literal

from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    env: Literal["dev", "prod"] = "dev"

    @property
    def is_dev(self) -> bool:
        return self.env == "dev"

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"
