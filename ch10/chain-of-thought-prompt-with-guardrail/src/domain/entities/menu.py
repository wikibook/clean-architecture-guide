from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Menu:
    menu_id: str
    name: str
    price: int
    category: str
    stock: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    def is_available(self, quantity: int) -> bool:
        return self.stock >= quantity

    def decrease_stock(self, quantity: int) -> None:
        if not self.is_available(quantity):
            raise ValueError("Insufficient stock")
        self.stock -= quantity
        self.updated_at = datetime.utcnow()
