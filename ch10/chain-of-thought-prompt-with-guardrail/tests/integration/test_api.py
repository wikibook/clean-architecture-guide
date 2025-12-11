from datetime import datetime, timezone
from typing import Generator
from unittest.mock import Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.domain.entities.menu import Menu
from src.domain.entities.order import Order
from src.domain.usecases.menu_usecases import GetMenuListUseCaseImpl
from src.domain.usecases.order_usecases import (
    CreateOrderUseCaseImpl,
    DeleteOrderUseCaseImpl,
    GetOrderStatusUseCaseImpl,
)
from src.presentation.controllers.menu_controller import MenuController
from src.presentation.controllers.order_controller import OrderController


@pytest.fixture
def mock_menu_repository() -> Generator[Mock, None, None]:
    with patch("src.domain.usecases.menu_usecases.MenuRepository") as mock:
        yield mock


@pytest.fixture
def mock_order_repository() -> Generator[Mock, None, None]:
    with patch("src.domain.usecases.order_usecases.OrderRepository") as mock:
        yield mock


@pytest.fixture
def test_app(mock_menu_repository: Mock, mock_order_repository: Mock) -> FastAPI:
    # Create use cases with mocked repositories
    get_menu_list_usecase = GetMenuListUseCaseImpl(menu_repository=mock_menu_repository)
    create_order_usecase = CreateOrderUseCaseImpl(
        order_repository=mock_order_repository,
        menu_repository=mock_menu_repository,
    )
    get_order_status_usecase = GetOrderStatusUseCaseImpl(
        order_repository=mock_order_repository
    )
    delete_order_usecase = DeleteOrderUseCaseImpl(
        order_repository=mock_order_repository
    )

    # Create controllers
    menu_controller = MenuController(get_menu_list_usecase=get_menu_list_usecase)
    order_controller = OrderController(
        create_order_usecase=create_order_usecase,
        get_order_status_usecase=get_order_status_usecase,
        delete_order_usecase=delete_order_usecase,
    )

    # Create test app
    test_app = FastAPI()
    test_app.include_router(menu_controller.register_routes())
    test_app.include_router(order_controller.register_routes())

    return test_app


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)


def test_get_menu_list(client: TestClient, mock_menu_repository: Mock) -> None:
    # Arrange
    menu1 = Menu(
        menu_id="menu-1",
        name="Americano",
        price=3000,
        category="coffee",
        stock=100,
        created_at=datetime.now(timezone.utc),
    )
    menu2 = Menu(
        menu_id="menu-2",
        name="Latte",
        price=4000,
        category="coffee",
        stock=100,
        created_at=datetime.now(timezone.utc),
    )
    mock_menu_repository.get_all.return_value = [menu1, menu2]

    # Act
    response = client.get("/menu")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]["menus"]) == 2
    assert data["data"]["menus"][0]["menu_id"] == "menu-1"
    assert data["data"]["menus"][0]["name"] == "Americano"


def test_create_order(
    client: TestClient, mock_menu_repository: Mock, mock_order_repository: Mock
) -> None:
    # Arrange
    menu = Menu(
        menu_id="menu-1",
        name="Americano",
        price=3000,
        category="coffee",
        stock=100,
        created_at=datetime.now(timezone.utc),
    )
    mock_menu_repository.get_by_id.return_value = menu

    # Act
    response = client.post(
        "/order",
        json={
            "customer_id": "cust-1",
            "menu_id": "menu-1",
            "quantity": 2,
            "options": {"size": "medium", "temperature": "hot"},
        },
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["status"] == "created"
    mock_menu_repository.get_by_id.assert_called_once_with("menu-1")
    mock_menu_repository.update.assert_called_once()
    mock_order_repository.save.assert_called_once()


def test_get_order_status(client: TestClient, mock_order_repository: Mock) -> None:
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
    mock_order_repository.get_by_id.return_value = order

    # Act
    response = client.get("/order/order-1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["order_id"] == "order-1"
    assert data["data"]["status"] == "preparing"
    mock_order_repository.get_by_id.assert_called_once_with("order-1")


def test_delete_order_success(client: TestClient, mock_order_repository: Mock) -> None:
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
    mock_order_repository.get_by_id.return_value = order
    mock_order_repository.delete.return_value = True

    # Act
    response = client.delete("/order/order-1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["order_id"] == "order-1"
    assert data["data"]["success"] is True
    assert data["data"]["message"] == "Order deleted successfully"
    mock_order_repository.delete.assert_called_once_with("order-1")


def test_delete_order_not_found(
    client: TestClient, mock_order_repository: Mock
) -> None:
    # Arrange
    mock_order_repository.get_by_id.return_value = None

    # Act
    response = client.delete("/order/invalid-order")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Order not found"
    mock_order_repository.delete.assert_not_called()
