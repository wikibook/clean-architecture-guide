from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch
from datetime import datetime
from src.main import app
from src.domain.entities.menu import Menu
from src.domain.entities.order import Order

client = TestClient(app)


@pytest.fixture
def mock_menu_repository():
    with patch('src.infrastructure.repositories.dynamodb_repositories.DynamoDBMenuRepository') as mock:
        yield mock


@pytest.fixture
def mock_order_repository():
    with patch('src.infrastructure.repositories.dynamodb_repositories.DynamoDBOrderRepository') as mock:
        yield mock


def test_get_menus(mock_menu_repository):
    # Arrange
    mock_menus = [
        Menu(menu_id="1", name="Americano", price=3000, category="coffee", stock=10),
        Menu(menu_id="2", name="Latte", price=4000, category="coffee", stock=10)
    ]
    mock_menu_repository.return_value.get_all.return_value = mock_menus
    
    # Act
    response = client.get("/menus")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 2
    assert response.json()["data"][0]["name"] == "Americano"


def test_create_order(mock_menu_repository, mock_order_repository):
    # Arrange
    menu = Menu(menu_id="1", name="Americano", price=3000, category="coffee", stock=10)
    mock_menu_repository.return_value.get_by_id.return_value = menu
    
    # Act
    response = client.post(
        "/orders",
        json={
            "customer_id": "cust-1",
            "menu_id": "1",
            "quantity": 2,
            "options": {"size": "medium"}
        }
    )
    
    # Assert
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert "order_id" in response.json()["data"]
    assert response.json()["data"]["status"] == "created"


def test_get_order(mock_order_repository):
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
    mock_order_repository.return_value.get_by_id.return_value = mock_order
    
    # Act
    response = client.get("/orders/order-1")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["order_id"] == "order-1"
    assert response.json()["data"]["status"] == "created"