import unittest
from datetime import datetime, timezone
from unittest.mock import Mock

from src.domain.dtos.order_dtos import CreateOrderRequestDTO
from src.domain.entities.menu import Menu
from src.domain.entities.order import Order
from src.domain.usecases.order_usecases import (
    CreateOrderUseCaseImpl,
    DeleteOrderUseCaseImpl,
    GetOrderStatusUseCaseImpl,
)


class TestOrderUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.order_repository = Mock()
        self.menu_repository = Mock()
        self.create_order_usecase = CreateOrderUseCaseImpl(
            order_repository=self.order_repository,
            menu_repository=self.menu_repository,
        )
        self.get_order_status_usecase = GetOrderStatusUseCaseImpl(
            order_repository=self.order_repository
        )
        self.delete_order_usecase = DeleteOrderUseCaseImpl(
            order_repository=self.order_repository
        )

    def test_create_order_success(self) -> None:
        # Arrange
        menu = Menu(
            menu_id="menu-1",
            name="Americano",
            price=3000,
            category="coffee",
            stock=100,
            created_at=datetime.now(timezone.utc),
        )
        self.menu_repository.get_by_id.return_value = menu

        request = CreateOrderRequestDTO(
            customer_id="cust-1",
            menu_id="menu-1",
            quantity=2,
            options={"size": "medium", "temperature": "hot"},
        )

        # Act
        result = self.create_order_usecase.execute(request)

        # Assert
        self.assertEqual(result.status, "created")
        self.menu_repository.get_by_id.assert_called_once_with("menu-1")
        self.menu_repository.update.assert_called_once()
        self.order_repository.save.assert_called_once()

    def test_create_order_invalid_menu_id(self) -> None:
        # Arrange
        self.menu_repository.get_by_id.return_value = None
        request = CreateOrderRequestDTO(
            customer_id="cust-1",
            menu_id="invalid-id",
            quantity=2,
            options={"size": "medium", "temperature": "hot"},
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.create_order_usecase.execute(request)
        self.assertEqual(str(context.exception), "Invalid menu ID")

    def test_create_order_insufficient_stock(self) -> None:
        # Arrange
        menu = Menu(
            menu_id="menu-1",
            name="Americano",
            price=3000,
            category="coffee",
            stock=1,
            created_at=datetime.now(timezone.utc),
        )
        self.menu_repository.get_by_id.return_value = menu
        request = CreateOrderRequestDTO(
            customer_id="cust-1",
            menu_id="menu-1",
            quantity=2,
            options={"size": "medium", "temperature": "hot"},
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.create_order_usecase.execute(request)
        self.assertEqual(str(context.exception), "Insufficient stock")

    def test_get_order_status_success(self) -> None:
        # Arrange
        order = Order(
            order_id="order-1",
            customer_id="cust-1",
            menu_id="menu-1",
            quantity=2,
            status="preparing",
            options={"size": "medium", "temperature": "hot"},
            created_at=datetime.now(timezone.utc),
        )
        self.order_repository.get_by_id.return_value = order

        # Act
        result = self.get_order_status_usecase.execute("order-1")

        # Assert
        assert result is not None  # Type guard
        self.assertEqual(result.order_id, "order-1")
        self.assertEqual(result.status, "preparing")
        self.order_repository.get_by_id.assert_called_once_with("order-1")

    def test_get_order_status_not_found(self) -> None:
        # Arrange
        self.order_repository.get_by_id.return_value = None

        # Act
        result = self.get_order_status_usecase.execute("invalid-order")

        # Assert
        self.assertIsNone(result)
        self.order_repository.get_by_id.assert_called_once_with("invalid-order")

    def test_delete_order_success(self) -> None:
        # Arrange
        order = Order(
            order_id="order-1",
            customer_id="cust-1",
            menu_id="menu-1",
            quantity=2,
            status="preparing",
            options={"size": "medium", "temperature": "hot"},
            created_at=datetime.now(timezone.utc),
        )
        self.order_repository.get_by_id.return_value = order
        self.order_repository.delete.return_value = True

        # Act
        result = self.delete_order_usecase.execute("order-1")

        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.order_id, "order-1")
        self.assertEqual(result.message, "Order deleted successfully")
        self.order_repository.delete.assert_called_once_with("order-1")

    def test_delete_order_not_found(self) -> None:
        # Arrange
        self.order_repository.get_by_id.return_value = None

        # Act
        result = self.delete_order_usecase.execute("invalid-order")

        # Assert
        self.assertFalse(result.success)
        self.assertEqual(result.order_id, "invalid-order")
        self.assertEqual(result.message, "Order not found")
        self.order_repository.delete.assert_not_called()
