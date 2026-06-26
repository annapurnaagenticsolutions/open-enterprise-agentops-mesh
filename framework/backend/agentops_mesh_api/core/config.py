from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Open Enterprise AgentOps Mesh API"
    app_version: str = "2.8.0"
    deterministic_mode: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()



# v0.4 uses local JSON storage by default so that the project remains easy to run,
# inspect, fork, and evolve before introducing external databases.
DEFAULT_DATA_DIR = "data"
