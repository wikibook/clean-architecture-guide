from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime
from enum import Enum, auto

class OrderStatus(Enum):
    CREATED = auto()
    PREPARING = auto()
    COMPLETED = auto()
    CANCELLED = auto()

@dataclass
class Order:
    order_id: str
    customer_id: str
    menu_id: str
    quantity: int
    status: OrderStatus
    options: Dict[str, str]
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def create(cls, order_id: str, customer_id: str, menu_id: str, 
              quantity: int, options: Dict[str, str]) -> 'Order':
        """새로운 주문 생성"""
        now = datetime.utcnow()
        return cls(
            order_id=order_id,
            customer_id=customer_id,
            menu_id=menu_id,
            quantity=quantity,
            status=OrderStatus.CREATED,
            options=options,
            created_at=now,
            updated_at=now
        )

    def update_status(self, status: OrderStatus) -> None:
        """주문 상태 업데이트"""
        self.status = status
        self.updated_at = datetime.utcnow()