import uuid
from ..interfaces.boundaries import (
    CreateOrderInputBoundary, GetOrderInputBoundary,
    CreateOrderInputDTO, GetOrderInputDTO, OrderOutputDTO
)
from ..interfaces.repositories import OrderRepository, MenuRepository


class CreateOrderUseCase(CreateOrderInputBoundary):
    def __init__(self, order_repository: OrderRepository, menu_repository: MenuRepository):
        self._order_repository = order_repository
        self._menu_repository = menu_repository

    def execute(self, input_dto: CreateOrderInputDTO) -> OrderOutputDTO:
        menu = self._menu_repository.get_by_id(input_dto.menu_id)
        if not menu:
            raise ValueError("Invalid menu ID")
            
        if not menu.has_sufficient_stock(input_dto.quantity):
            raise ValueError("Insufficient stock")
            
        order = Order.create(
            order_id=f"order-{uuid.uuid4()}",
            customer_id=input_dto.customer_id,
            menu_id=input_dto.menu_id,
            quantity=input_dto.quantity,
            options=input_dto.options
        )
        
        menu.decrease_stock(input_dto.quantity)
        self._menu_repository.update(menu)
        self._order_repository.create(order)
        
        return OrderOutputDTO(
            order_id=order.order_id,
            status=order.status,
            created_at=order.created_at
        )


class GetOrderUseCase(GetOrderInputBoundary):
    def __init__(self, order_repository: OrderRepository):
        self._order_repository = order_repository

    def execute(self, input_dto: GetOrderInputDTO) -> OrderOutputDTO:
        order = self._order_repository.get_by_id(input_dto.order_id)
        if not order:
            raise ValueError("Order not found")
            
        return OrderOutputDTO(
            order_id=order.order_id,
            status=order.status,
            created_at=order.created_at
        )