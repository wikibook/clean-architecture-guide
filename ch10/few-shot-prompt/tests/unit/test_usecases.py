import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock

from src.domain.entities import Menu, Order, MenuCategory, OrderStatus
from src.application.usecases import (
    GetMenuListUseCase,
    CreateOrderUseCase,
    GetOrderStatusUseCase,
)
from src.application.exceptions import (
    MenuNotFoundError,
    InsufficientStockError,
    OrderNotFoundError,
    DatabaseError,
)


@pytest.fixture
def menu_repository():
    return Mock()


@pytest.fixture
def order_repository():
    return Mock()


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


@pytest.mark.asyncio
async def test_get_menu_list_success(menu_repository, sample_menu):
    # Given
    menu_repository.get_all = AsyncMock(return_value=[sample_menu])
    usecase = GetMenuListUseCase(menu_repository)

    # When
    result = await usecase.execute()

    # Then
    assert len(result) == 1
    assert result[0].menu_id == sample_menu.menu_id
    menu_repository.get_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_menu_list_database_error(menu_repository):
    # Given
    menu_repository.get_all = AsyncMock(side_effect=Exception("DB Error"))
    usecase = GetMenuListUseCase(menu_repository)

    # When/Then
    with pytest.raises(DatabaseError):
        await usecase.execute()


@pytest.mark.asyncio
async def test_create_order_success(
    menu_repository, order_repository, sample_menu, sample_order
):
    # Given
    menu_repository.get_by_id = AsyncMock(return_value=sample_menu)
    menu_repository.update_stock = AsyncMock(return_value=True)
    order_repository.create = AsyncMock(return_value=sample_order)
    usecase = CreateOrderUseCase(menu_repository, order_repository)

    # When
    result = await usecase.execute(
        customer_id="customer-1",
        menu_id="menu-1",
        quantity=2,
        options={"size": "medium", "temperature": "hot"},
    )

    # Then
    assert result.order_id == sample_order.order_id
    assert result.status == OrderStatus.CREATED
    menu_repository.get_by_id.assert_called_once_with("menu-1")
    menu_repository.update_stock.assert_called_once_with("menu-1", -2)
    order_repository.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_order_menu_not_found(menu_repository, order_repository):
    # Given
    menu_repository.get_by_id = AsyncMock(return_value=None)
    usecase = CreateOrderUseCase(menu_repository, order_repository)

    # When/Then
    with pytest.raises(MenuNotFoundError):
        await usecase.execute(
            customer_id="customer-1",
            menu_id="invalid-menu",
            quantity=2,
            options={"size": "medium", "temperature": "hot"},
        )


@pytest.mark.asyncio
async def test_create_order_insufficient_stock(
    menu_repository, order_repository, sample_menu
):
    # Given
    menu_repository.get_by_id = AsyncMock(return_value=sample_menu)
    usecase = CreateOrderUseCase(menu_repository, order_repository)

    # When/Then
    with pytest.raises(InsufficientStockError):
        await usecase.execute(
            customer_id="customer-1",
            menu_id="menu-1",
            quantity=20,  # 재고보다 많은 수량
            options={"size": "medium", "temperature": "hot"},
        )


@pytest.mark.asyncio
async def test_get_order_status_success(order_repository, sample_order):
    # Given
    order_repository.get_by_id = AsyncMock(return_value=sample_order)
    usecase = GetOrderStatusUseCase(order_repository)

    # When
    result = await usecase.execute("order-1")

    # Then
    assert result.order_id == sample_order.order_id
    assert result.status == sample_order.status
    order_repository.get_by_id.assert_called_once_with("order-1")


@pytest.mark.asyncio
async def test_get_order_status_not_found(order_repository):
    # Given
    order_repository.get_by_id = AsyncMock(return_value=None)
    usecase = GetOrderStatusUseCase(order_repository)

    # When/Then
    with pytest.raises(OrderNotFoundError):
        await usecase.execute("invalid-order")