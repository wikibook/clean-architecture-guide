import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# 환경 변수에서 데이터베이스 설정 읽기
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql://root:password@localhost:3306/coffee_order"  # 기본값
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """데이터베이스 세션을 생성하고 관리하는 의존성 주입 함수"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
