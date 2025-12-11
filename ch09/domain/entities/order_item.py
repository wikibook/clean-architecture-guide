from ..value_objects.money import Money


class OrderItem:
    def __init__(self, id: str, order_id: str, coffee_id: str, quantity: int, unit_price: Money):
        self.id = id
        self.order_id = order_id
        self.coffee_id = coffee_id
        self.quantity = quantity
        self.unit_price = unit_price

    def calculate_subtotal(self) -> Money:
        """주문 항목의 단가와 수량을 곱해 소계를 계산한다"""
        return self.unit_price * self.quantity
