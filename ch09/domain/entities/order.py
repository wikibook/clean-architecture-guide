from datetime import datetime
from typing import List
from ..value_objects.money import Money
from ..value_objects.order_status import OrderStatus
from .order_item import OrderItem
from .coffee import Coffee
from domain.shared.aggregate_root import AggregateRoot
from domain.events.order_events import OrderCreated, OrderItemAdded, OrderStatusChanged


class Order(AggregateRoot):
    def __init__(self, id: str, customer_id: str):
        super().__init__()
        self.id = id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []
        self.total_amount = Money(amount=0)
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
        self._record_event(OrderCreated(order_id=self.id, customer_id=self.customer_id))

    def add_coffee(self, coffee: Coffee, quantity: int) -> None:
        """고객이 특정 커피를 원하는 수량만큼 주문 목록에 추가한다"""
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
        self._record_event(
            OrderItemAdded(order_id=self.id, item_id=order_item.id, coffee_id=coffee.id, quantity=quantity)
        )

    def calculate_total(self) -> Money:
        """주문에 담긴 모든 항목의 금액을 합산하여 총액을 계산한다"""
        total = Money(amount=0)
        for item in self.items:
            total = total + item.calculate_subtotal()
        self.total_amount = total
        return self.total_amount

    def change_status(self, new_status: OrderStatus) -> None:
        """주문 처리 단계가 진행되면서 상태를 변경한다 (결제승인→준비중→완료 등)"""
        if self.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
            raise ValueError("완료/취소된 주문은 상태 변경 불가")
        if new_status == OrderStatus.PENDING:
            raise ValueError("PENDING으로 되돌릴 수 없습니다")
        previous = self.status
        self.status = new_status
        self._record_event(
            OrderStatusChanged(order_id=self.id, previous_status=previous.value, new_status=new_status.value)
        )

    def can_cancel(self) -> bool:
        """고객이 주문을 취소할 수 있는지 확인한다 (아직 처리 시작 전인 경우만 가능)"""
        return self.status == OrderStatus.PENDING
