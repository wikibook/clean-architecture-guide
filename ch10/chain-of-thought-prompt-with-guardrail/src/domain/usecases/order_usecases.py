import uuid
from abc import ABC, abstractmethod
from typing import Optional

from ..dtos.order_dtos import (
    CreateOrderRequestDTO,
    DeleteOrderResponseDTO,
    OrderResponseDTO,
)
from ..entities.order import Order
from ..repositories.menu_repository import MenuRepository
from ..repositories.order_repository import OrderRepository


class CreateOrderUseCase(ABC):
    @abstractmethod
    def execute(self, request: CreateOrderRequestDTO) -> OrderResponseDTO:
        pass


class GetOrderStatusUseCase(ABC):
    @abstractmethod
    def execute(self, order_id: str) -> Optional[OrderResponseDTO]:
        pass


class DeleteOrderUseCase(ABC):
    @abstractmethod
    def execute(self, order_id: str) -> DeleteOrderResponseDTO:
        pass


class CreateOrderUseCaseImpl(CreateOrderUseCase):
    def __init__(
        self,
        order_repository: OrderRepository,
        menu_repository: MenuRepository,
    ) -> None:
        self.order_repository = order_repository
        self.menu_repository = menu_repository

    def execute(self, request: CreateOrderRequestDTO) -> OrderResponseDTO:
        menu = self.menu_repository.get_by_id(request.menu_id)
        if not menu:
            raise ValueError("Invalid menu ID")

        if not menu.is_available(request.quantity):
            raise ValueError("Insufficient stock")

        order = Order.create(
            order_id=str(uuid.uuid4()),
            customer_id=request.customer_id,
            menu_id=request.menu_id,
            quantity=request.quantity,
            options=request.options,
        )

        menu.decrease_stock(request.quantity)
        self.menu_repository.update(menu)
        self.order_repository.save(order)

        return OrderResponseDTO(
            order_id=order.order_id,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


class GetOrderStatusUseCaseImpl(GetOrderStatusUseCase):
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    def execute(self, order_id: str) -> Optional[OrderResponseDTO]:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return None

        return OrderResponseDTO(
            order_id=order.order_id,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )


class DeleteOrderUseCaseImpl(DeleteOrderUseCase):
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    def execute(self, order_id: str) -> DeleteOrderResponseDTO:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return DeleteOrderResponseDTO(
                order_id=order_id,
                success=False,
                message="Order not found",
            )

        success = self.order_repository.delete(order_id)
        return DeleteOrderResponseDTO(
            order_id=order_id,
            success=success,
            message=(
                "Order deleted successfully" if success else "Failed to delete order"
            ),
        )
