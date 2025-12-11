from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CustomerModel(Base):
    """고객 테이블 모델"""

    customer_id: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
