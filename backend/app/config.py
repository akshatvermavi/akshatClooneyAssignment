import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    api_prefix: str = "/api"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./asana_clone.db")
    asana_seed_workspace_name: str = os.getenv("ASANA_SEED_WORKSPACE_NAME", "Demo Workspace")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
