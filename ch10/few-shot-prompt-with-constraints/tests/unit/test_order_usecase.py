import unittest
from unittest.mock import Mock
from datetime import datetime
from src.domain.entities.menu import Menu
from src.domain.entities.order import Order
from src.domain.usecases.order_usecases import CreateOrderUseCase, GetOrderUseCase
from src.domain.interfaces.boundaries import CreateOrderInputDTO, GetOrderInputDTO


class TestCreateOrderUseCase(unittest.TestCase):
    def setUp(self):
        self.order_repository = Mock()
        self.menu_repository = Mock()
        self.usecase = CreateOrderUseCase(
            order_repository=self.order_repository,
            menu_repository=self.menu_repository
        )
        
    def test_execute_creates_order_successfully(self):
        # Arrange
        menu = Menu(menu_id="1", name="Americano", price=3000, category="coffee", stock=10)
        self.menu_repository.get_by_id.return_value = menu
        
        input_dto = CreateOrderInputDTO(
            customer_id="cust-1",
            menu_id="1",
            quantity=2,
            options={"size": "medium"}
        )
        
        # Act
        result = self.usecase.execute(input_dto)
        
        # Assert
        self.assertIsNotNone(result.order_id)
        self.assertEqual(result.status, "created")
        self.menu_repository.get_by_id.assert_called_once_with("1")
        self.menu_repository.update.assert_called_once()
        self.order_repository.create.assert_called_once()
        
    def test_execute_raises_error_for_invalid_menu(self):
        # Arrange
        self.menu_repository.get_by_id.return_value = None
        
        input_dto = CreateOrderInputDTO(
            customer_id="cust-1",
            menu_id="invalid",
            quantity=2,
            options={"size": "medium"}
        )
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.usecase.execute(input_dto)
        
        self.assertEqual(str(context.exception), "Invalid menu ID")
        
    def test_execute_raises_error_for_insufficient_stock(self):
        # Arrange
        menu = Menu(menu_id="1", name="Americano", price=3000, category="coffee", stock=1)
        self.menu_repository.get_by_id.return_value = menu
        
        input_dto = CreateOrderInputDTO(
            customer_id="cust-1",
            menu_id="1",
            quantity=2,
            options={"size": "medium"}
        )
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.usecase.execute(input_dto)
        
        self.assertEqual(str(context.exception), "Insufficient stock")


class TestGetOrderUseCase(unittest.TestCase):
    def setUp(self):
        self.order_repository = Mock()
        self.usecase = GetOrderUseCase(self.order_repository)
        
    def test_execute_returns_order(self):
        # Arrange
        mock_order = Order(
            order_id="order-1",
            customer_id="cust-1",
            menu_id="1",
            quantity=2,
            status="created",
            options={"size": "medium"},
            created_at=datetime.utcnow()
        )
        self.order_repository.get_by_id.return_value = mock_order
        
        input_dto = GetOrderInputDTO(order_id="order-1")
        
        # Act
        result = self.usecase.execute(input_dto)
        
        # Assert
        self.assertEqual(result.order_id, "order-1")
        self.assertEqual(result.status, "created")
        self.order_repository.get_by_id.assert_called_once_with("order-1")
        
    def test_execute_raises_error_for_not_found_order(self):
        # Arrange
        self.order_repository.get_by_id.return_value = None
        input_dto = GetOrderInputDTO(order_id="invalid")
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.usecase.execute(input_dto)
        
        self.assertEqual(str(context.exception), "Order not found")