from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	jwt_secret_key: str = "dev-secret-change-me"
	jwt_algorithm: str = "HS256"
	access_token_expire_minutes: int = 60 * 12
	cors_origins: List[str] = ["*"]

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
	return Settings()