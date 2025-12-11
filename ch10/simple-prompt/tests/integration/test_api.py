import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import patch, AsyncMock
from src.interfaces.api import app
from src.domain.entities import Menu, Order, OrderStatus

client = TestClient(app)

def test_get_menus():
    # Given
    expected_menus = [
        Menu(id="1", name="아메리카노", price=4500, category="커피", stock=100),
        Menu(id="2", name="카페라떼", price=5000, category="커피", stock=100)
    ]
    
    with patch('src.infrastructure.repositories.DynamoDBMenuRepository.get_all', 
               new_callable=AsyncMock) as mock_get_all:
        mock_get_all.return_value = expected_menus
        
        # When
        response = client.get("/menu")
        
        # Then
        assert response.status_code == 200
        menus = response.json()
        assert len(menus) == 2
        assert menus[0]["name"] == "아메리카노"
        assert menus[1]["name"] == "카페라떼"

def test_create_order():
    # Given
    order_data = {
        "customer_id": "customer-1",
        "menu_id": "1",
        "quantity": 2
    }
    
    expected_order = Order(
        id="test-id",
        customer_id="customer-1",
        menu_id="1",
        quantity=2,
        status=OrderStatus.PENDING,
        created_at=datetime.utcnow()
    )
    
    with patch('src.infrastructure.repositories.DynamoDBMenuRepository.get_by_id',
               new_callable=AsyncMock) as mock_get_menu:
        with patch('src.infrastructure.repositories.DynamoDBMenuRepository.update_stock',
                  new_callable=AsyncMock) as mock_update_stock:
            with patch('src.infrastructure.repositories.DynamoDBOrderRepository.create',
                      new_callable=AsyncMock) as mock_create_order:
                
                mock_get_menu.return_value = Menu(
                    id="1", name="아메리카노", price=4500, category="커피", stock=100
                )
                mock_update_stock.return_value = True
                mock_create_order.return_value = expected_order
                
                # When
                response = client.post("/order", json=order_data)
                
                # Then
                assert response.status_code == 200
                order = response.json()
                assert order["id"] == "test-id"
                assert order["status"] == "PENDING"