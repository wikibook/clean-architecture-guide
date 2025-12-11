import unittest
from unittest.mock import Mock
from datetime import datetime
from src.domain.entities.menu import Menu
from src.domain.entities.order import Order, OrderStatus
from src.domain.usecases.order_usecases import OrderUseCases
from src.domain.interfaces.boundaries import CreateOrderInputDTO, GetOrderInputDTO

class TestOrderUseCases(unittest.TestCase):
    def setUp(self):
        """테스트 설정"""
        self.order_repository = Mock()
        self.menu_repository = Mock()
        self.order_usecase = OrderUseCases(
            order_repository=self.order_repository,
            menu_repository=self.menu_repository
        )

    def test_create_order_success(self):
        """주문 생성 성공 테스트"""
        # Given
        menu = Menu(
            menu_id="menu-1",
            name="Americano",
            price=3000,
            category="coffee",
            stock=100,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.menu_repository.get_by_id.return_value = menu

        input_dto = CreateOrderInputDTO(
            customer_id="cust-1",
            menu_id="menu-1",
            quantity=2,
            options={"size": "medium"}
        )

        # When
        result = self.order_usecase.create_order(input_dto)

        # Then
        self.assertIsNotNone(result.order_id)
        self.assertEqual(result.status, OrderStatus.CREATED)
        self.menu_repository.update.assert_called_once()
        self.order_repository.create.assert_called_once()

    def test_create_order_menu_not_found(self):
        """존재하지 않는 메뉴로 주문 시도 테스트"""
        # Given
        self.menu_repository.get_by_id.return_value = None
        input_dto = CreateOrderInputDTO(
            customer_id="cust-1",
            menu_id="invalid-menu",
            quantity=2,
            options={"size": "medium"}
        )

        # When/Then
        with self.assertRaises(ValueError) as context:
            self.order_usecase.create_order(input_dto)
        self.assertEqual(str(context.exception), "Menu not found")

    def test_create_order_insufficient_stock(self):
        """재고 부족 테스트"""
        # Given
        menu = Menu(
            menu_id="menu-1",
            name="Americano",
            price=3000,
            category="coffee",
            stock=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.menu_repository.get_by_id.return_value = menu

        input_dto = CreateOrderInputDTO(
            customer_id="cust-1",
            menu_id="menu-1",
            quantity=2,
            options={"size": "medium"}
        )

        # When/Then
        with self.assertRaises(ValueError) as context:
            self.order_usecase.create_order(input_dto)
        self.assertEqual(str(context.exception), "Insufficient stock")

    def test_get_order_success(self):
        """주문 조회 성공 테스트"""
        # Given
        order = Order(
            order_id="order-1",
            customer_id="cust-1",
            menu_id="menu-1",
            quantity=2,
            status=OrderStatus.CREATED,
            options={"size": "medium"},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.order_repository.get_by_id.return_value = order
        input_dto = GetOrderInputDTO(order_id="order-1")

        # When
        result = self.order_usecase.get_order(input_dto)

        # Then
        self.assertEqual(result.order_id, "order-1")
        self.assertEqual(result.status, OrderStatus.CREATED)

    def test_get_order_not_found(self):
        """존재하지 않는 주문 조회 테스트"""
        # Given
        self.order_repository.get_by_id.return_value = None
        input_dto = GetOrderInputDTO(order_id="invalid-order")

        # When/Then
        with self.assertRaises(ValueError) as context:
            self.order_usecase.get_order(input_dto)
        self.assertEqual(str(context.exception), "Order not found")

if __name__ == '__main__':
    unittest.main()