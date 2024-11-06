# app/database/db_session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLAlchemy 엔진 생성: 데이터베이스 URL을 통해 연결
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/docsto"  # 환경 설정에 DATABASE_URL이 있다고 가정

# SQLAlchemy 엔진을 생성합니다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 로컬 객체를 생성합니다. 이 객체를 통해 세션을 관리합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 데이터베이스 세션을 반환하는 함수
# FastAPI에서 의존성 주입을 통해 세션을 관리할 때 사용됩니다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
