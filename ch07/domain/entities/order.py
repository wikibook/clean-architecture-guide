from datetime import datetime
from typing import List
from ..value_objects.money import Money
from ..value_objects.order_status import OrderStatus
from .order_item import OrderItem
from .coffee import Coffee


class Order:
    def __init__(self, id: str, customer_id: str):
        self.id = id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.total_amount = Money(amount=0)
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()

    def add_coffee(self, coffee: Coffee, quantity: int) -> None:
        if quantity <= 0 or quantity > 100:
            raise ValueError("수량은 1~100 사이여야 합니다")
        coffee.reserve_stock(quantity)
        order_item = OrderItem(
            id=f"item-{self.id}-{coffee.id}",
            order_id=self.id,
            coffee_id=coffee.id,
            quantity=quantity,
            unit_price=coffee.price,
        )
        self.items.append(order_item)
        self.calculate_total()

    def calculate_total(self) -> Money:
        total = Money(amount=0)
        for item in self.items:
            total = total + item.calculate_subtotal()
        self.total_amount = total
        return self.total_amount

    def change_status(self, new_status: OrderStatus) -> None:
        if self.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            raise ValueError("완료/취소된 주문은 상태 변경 불가")
        if new_status == OrderStatus.PENDING:
            raise ValueError("PENDING으로 되돌릴 수 없습니다")
        self.status = new_status

    def can_cancel(self) -> bool:
        return self.status == OrderStatus.PENDING
