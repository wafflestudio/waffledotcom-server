import pydantic


class DBConfig(pydantic.BaseSettings):
    username: str = pydantic.Field(..., env="USERNAME")
    password: str = pydantic.Field(..., env="PASSWORD")
    host: str = pydantic.Field(..., env="HOST")
    port: int = pydantic.Field(..., env="PORT")
    database: str = pydantic.Field(..., env="DATABASE")

    @property
    def url(self) -> str:
        return f"mysql+mysqldb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    class Config:
        case_sensitive = False
        env_file = "../.env"
