import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str  # 예시: "postgresql://user:password@localhost/dbname"

    class Config:
        env_file = ".env"  # .env 파일을 로드하도록 설정


# Settings 인스턴스 생성
settings = Settings()
