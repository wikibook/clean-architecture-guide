import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from src.interfaces.api import app
from src.domain.entities import Menu, Order, MenuCategory, OrderStatus
from datetime import datetime


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_menu():
    return Menu(
        menu_id="menu-1",
        name="Americano",
        price=3000,
        category=MenuCategory.COFFEE,
        stock=10,
    )


@pytest.fixture
def sample_order():
    return Order(
        order_id="order-1",
        customer_id="customer-1",
        menu_id="menu-1",
        quantity=2,
        options={"size": "medium", "temperature": "hot"},
        status=OrderStatus.CREATED,
        created_at=datetime.utcnow(),
    )


def test_get_menu_list_success(client, sample_menu):
    # Given
    with patch(
        "src.application.usecases.GetMenuListUseCase.execute",
        new_callable=AsyncMock,
        return_value=[sample_menu],
    ):
        # When
        response = client.get("/menu")

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 1
        assert data["data"][0]["menu_id"] == sample_menu.menu_id
        assert data["message"] == "Menus retrieved successfully"


def test_create_order_success(client, sample_order):
    # Given
    with patch(
        "src.application.usecases.CreateOrderUseCase.execute",
        new_callable=AsyncMock,
        return_value=sample_order,
    ):
        # When
        response = client.post(
            "/order",
            json={
                "customer_id": "customer-1",
                "menu_id": "menu-1",
                "quantity": 2,
                "options": {"size": "medium", "temperature": "hot"},
            },
        )

        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["order_id"] == sample_order.order_id
        assert data["message"] == "Order created successfully"


def test_create_order_invalid_menu(client):
    # Given
    with patch(
        "src.application.usecases.CreateOrderUseCase.execute",
        new_callable=AsyncMock,
        side_effect=MenuNotFoundError("Invalid menu ID"),
    ):
        # When
        response = client.post(
            "/order",
            json={
                "customer_id": "customer-1",
                "menu_id": "invalid-menu",
                "quantity": 2,
                "options": {"size": "medium", "temperature": "hot"},
            },
        )

        # Then
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Invalid menu ID"


def test_get_order_status_success(client, sample_order):
    # Given
    with patch(
        "src.application.usecases.GetOrderStatusUseCase.execute",
        new_callable=AsyncMock,
        return_value=sample_order,
    ):
        # When
        response = client.get(f"/order/{sample_order.order_id}")

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["order_id"] == sample_order.order_id
        assert data["message"] == "Order status retrieved successfully"


def test_get_order_status_not_found(client):
    # Given
    with patch(
        "src.application.usecases.GetOrderStatusUseCase.execute",
        new_callable=AsyncMock,
        side_effect=OrderNotFoundError("Order not found"),
    ):
        # When
        response = client.get("/order/invalid-order")

        # Then
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Order not found"