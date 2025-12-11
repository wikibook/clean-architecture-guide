from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """모든 SQLAlchemy 모델의 기본 클래스"""

    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        """테이블 이름을 클래스 이름의 소문자 버전으로 자동 생성"""
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
