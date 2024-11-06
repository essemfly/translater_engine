# app/database/alembic.py
from app.database import Base

# alembic.ini에서 설정하는 DATABASE_URL을 사용하여 데이터베이스 연결을 구성합니다.
# 환경 변수나 settings에서 가져올 수도 있습니다.
# 예시에서는 settings.py로 가정하여 사용합니다.

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Alembic 설정을 위해 `Base.metadata`를 참조할 수 있도록 함.
# 이 값은 Alembic이 마이그레이션 파일을 생성하는데 필요한 메타데이터입니다.
target_metadata = Base.metadata

# Alembic은 자동으로 이 파일을 사용하여 마이그레이션을 처리합니다.
