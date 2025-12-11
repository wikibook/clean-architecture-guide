import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from src.domain.entities import Menu, Order, OrderStatus
from src.application.usecases import MenuService, OrderService

@pytest.fixture
def menu_repository():
    return Mock()

@pytest.fixture
def order_repository():
    return Mock()

@pytest.fixture
def menu_service(menu_repository):
    return MenuService(menu_repository)

@pytest.fixture
def order_service(order_repository, menu_repository):
    return OrderService(order_repository, menu_repository)

@pytest.mark.asyncio
async def test_get_all_menus(menu_service, menu_repository):
    # Given
    expected_menus = [
        Menu(id="1", name="아메리카노", price=4500, category="커피", stock=100),
        Menu(id="2", name="카페라떼", price=5000, category="커피", stock=100)
    ]
    menu_repository.get_all = AsyncMock(return_value=expected_menus)

    # When
    menus = await menu_service.get_all_menus()

    # Then
    assert menus == expected_menus
    menu_repository.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_create_order_success(order_service, menu_repository, order_repository):
    # Given
    menu = Menu(id="1", name="아메리카노", price=4500, category="커피", stock=100)
    menu_repository.get_by_id = AsyncMock(return_value=menu)
    menu_repository.update_stock = AsyncMock(return_value=True)
    
    expected_order = Order(
        id="test-id",
        customer_id="customer-1",
        menu_id="1",
        quantity=2,
        status=OrderStatus.PENDING,
        created_at=datetime.utcnow()
    )
    order_repository.create = AsyncMock(return_value=expected_order)

    # When
    order = await order_service.create_order("customer-1", "1", 2)

    # Then
    assert order == expected_order
    menu_repository.get_by_id.assert_called_once_with("1")
    menu_repository.update_stock.assert_called_once_with("1", 2)
    order_repository.create.assert_called_once()