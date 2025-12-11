from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Menu:
    menu_id: str
    name: str
    price: int
    category: str
    stock: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_available(self, quantity: int) -> bool:
        """주문 가능한 재고가 있는지 확인"""
        return self.stock >= quantity

    def decrease_stock(self, quantity: int) -> None:
        """재고 감소"""
        if not self.is_available(quantity):
            raise ValueError("Insufficient stock")
        self.stock -= quantity
        self.updated_at = datetime.utcnow()