from datetime import datetime, timezone
from typing import Generator
from unittest.mock import Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.domain.entities.customer import Customer
from src.domain.usecases.customer_usecases import GetCustomerUseCaseImpl
from src.presentation.controllers.customer_controller import CustomerController


@pytest.fixture
def mock_customer_repository() -> Generator[Mock, None, None]:
    with patch(
        "src.infrastructure.repositories.dynamodb_customer_repository.DynamoDBCustomerRepository"
    ) as mock:
        instance = mock.return_value
        yield instance


@pytest.fixture
def test_app(mock_customer_repository: Mock) -> FastAPI:
    # Create use case with mocked repository
    get_customer_usecase = GetCustomerUseCaseImpl(
        customer_repository=mock_customer_repository
    )

    # Create controller
    customer_controller = CustomerController(get_customer_usecase=get_customer_usecase)

    # Create test app
    test_app = FastAPI()
    test_app.include_router(customer_controller.register_routes())

    return test_app


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)


def test_get_customer_success(
    client: TestClient, mock_customer_repository: Mock
) -> None:
    # Arrange
    customer = Customer(
        customer_id="cust-1",
        name="John Doe",
        email="john@example.com",
        phone="+1234567890",
        created_at=datetime.now(timezone.utc),
    )
    mock_customer_repository.get_by_id.return_value = customer

    # Act
    response = client.get("/customer/cust-1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["customer_id"] == "cust-1"
    assert data["data"]["name"] == "John Doe"
    assert data["data"]["email"] == "john@example.com"
    assert data["data"]["phone"] == "+1234567890"
    mock_customer_repository.get_by_id.assert_called_once_with("cust-1")


def test_get_customer_not_found(
    client: TestClient, mock_customer_repository: Mock
) -> None:
    # Arrange
    mock_customer_repository.get_by_id.return_value = None

    # Act
    response = client.get("/customer/non-existent-id")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Customer not found"
    mock_customer_repository.get_by_id.assert_called_once_with("non-existent-id")
