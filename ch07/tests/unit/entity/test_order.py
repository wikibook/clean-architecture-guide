import unittest

from domain.entities.order import Order
from domain.entities.coffee import Coffee
from domain.value_objects.money import Money


class TestOrder(unittest.TestCase):
    def test_add_coffee(self):
        # Given
        coffee = Coffee(id="coffee-1", name="Latte", price=Money(500), stock=10)
        order = Order(id="order-1", customer_id="cust-1")

        # When
        order.add_coffee(coffee, 2)

        # Then
        self.assertEqual(len(order.items), 1)  # (1) 항목 추가 확인
        self.assertEqual(order.items[0].quantity, 2)  # (2) 수량 확인
        self.assertEqual(order.total_amount.amount, 1000)  # (3) 총액 확인
        self.assertEqual(coffee.stock, 8)  # (4) 재고 감소 확인


if __name__ == "__main__":
    unittest.main()
