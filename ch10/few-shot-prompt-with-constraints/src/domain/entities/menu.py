from dataclasses import dataclass
from typing import Optional


@dataclass
class Menu:
    menu_id: str
    name: str
    price: int
    category: str
    stock: int
    
    def has_sufficient_stock(self, quantity: int) -> bool:
        return self.stock >= quantity

    def decrease_stock(self, quantity: int) -> None:
        if not self.has_sufficient_stock(quantity):
            raise ValueError("Insufficient stock")
        self.stock -= quantity