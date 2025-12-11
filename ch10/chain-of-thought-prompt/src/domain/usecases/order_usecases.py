import uuid
from typing import Optional
from ..interfaces.boundaries import (
    OrderInputBoundary, CreateOrderInputDTO, 
    GetOrderInputDTO, OrderOutputDTO
)
from ..interfaces.repositories import OrderRepository, MenuRepository
from ..entities.order import Order

class OrderUseCases(OrderInputBoundary):
    def __init__(
        self, 
        order_repository: OrderRepository,
        menu_repository: MenuRepository
    ):
        self._order_repository = order_repository
        self._menu_repository = menu_repository

    def create_order(self, input_dto: CreateOrderInputDTO) -> OrderOutputDTO:
        """주문 생성"""
        # 메뉴 존재 여부 확인
        menu = self._menu_repository.get_by_id(input_dto.menu_id)
        if not menu:
            raise ValueError("Menu not found")

        # 재고 확인
        if not menu.is_available(input_dto.quantity):
            raise ValueError("Insufficient stock")

        # 주문 생성
        order = Order.create(
            order_id=str(uuid.uuid4()),
            customer_id=input_dto.customer_id,
            menu_id=input_dto.menu_id,
            quantity=input_dto.quantity,
            options=input_dto.options
        )

        # 재고 감소
        menu.decrease_stock(input_dto.quantity)
        self._menu_repository.update(menu)

        # 주문 저장
        self._order_repository.create(order)

        return OrderOutputDTO(
            order_id=order.order_id,
            status=order.status,
            created_at=order.created_at
        )

    def get_order(self, input_dto: GetOrderInputDTO) -> OrderOutputDTO:
        """주문 조회"""
        order = self._order_repository.get_by_id(input_dto.order_id)
        if not order:
            raise ValueError("Order not found")

        return OrderOutputDTO(
            order_id=order.order_id,
            status=order.status,
            created_at=order.created_at
        )