import unittest
from datetime import datetime, timezone
from unittest.mock import Mock

from src.domain.entities.customer import Customer
from src.domain.usecases.customer_usecases import GetCustomerUseCaseImpl


class TestCustomerUseCase(unittest.TestCase):
    def setUp(self) -> None:
        self.customer_repository = Mock()
        self.get_customer_usecase = GetCustomerUseCaseImpl(
            customer_repository=self.customer_repository
        )

    def test_get_customer_success(self) -> None:
        # Arrange
        customer = Customer(
            customer_id="cust-1",
            name="John Doe",
            email="john@example.com",
            phone="+1234567890",
            created_at=datetime.now(timezone.utc),
        )
        self.customer_repository.get_by_id.return_value = customer

        # Act
        result = self.get_customer_usecase.execute("cust-1")

        # Assert
        assert result is not None  # Type guard
        self.assertEqual(result.customer_id, "cust-1")
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.email, "john@example.com")
        self.assertEqual(result.phone, "+1234567890")
        self.customer_repository.get_by_id.assert_called_once_with("cust-1")

    def test_get_customer_not_found(self) -> None:
        # Arrange
        self.customer_repository.get_by_id.return_value = None

        # Act
        result = self.get_customer_usecase.execute("non-existent-id")

        # Assert
        self.assertIsNone(result)
        self.customer_repository.get_by_id.assert_called_once_with("non-existent-id")
