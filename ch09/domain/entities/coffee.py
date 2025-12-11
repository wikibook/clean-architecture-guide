from typing import Optional
from ..value_objects.money import Money


class Coffee:
    def __init__(self, id: str, name: str, price: Money, description: Optional[str] = None, stock: int = 0):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock

    def is_available(self) -> bool:
        """고객이 주문 가능한 재고가 있는지 확인한다"""
        return self.stock > 0

    def reserve_stock(self, quantity: int) -> None:
        """주문 처리를 위해 요청된 수량만큼 재고를 예약한다"""
        if quantity <= 0:
            raise ValueError("수량은 1 이상이어야 합니다")
        if quantity > self.stock:
            raise ValueError(f"재고 부족: {self.name} (남은 수량: {self.stock})")
        self.stock -= quantity
