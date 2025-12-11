from typing import List, Optional
from datetime import datetime
from pynamodb.exceptions import DoesNotExist
from src.domain.entities import Menu, Order, OrderStatus
from src.domain.repositories import MenuRepository, OrderRepository
from .models import MenuModel, OrderModel

class DynamoDBMenuRepository(MenuRepository):
    async def get_all(self) -> List[Menu]:
        return [
            Menu(
                id=item.id,
                name=item.name,
                price=item.price,
                category=item.category,
                stock=item.stock
            )
            for item in MenuModel.scan()
        ]

    async def get_by_id(self, menu_id: str) -> Optional[Menu]:
        try:
            item = MenuModel.get(menu_id)
            return Menu(
                id=item.id,
                name=item.name,
                price=item.price,
                category=item.category,
                stock=item.stock
            )
        except DoesNotExist:
            return None

    async def update_stock(self, menu_id: str, quantity: int) -> bool:
        try:
            menu = MenuModel.get(menu_id)
            if menu.stock >= quantity:
                menu.stock -= quantity
                menu.save()
                return True
            return False
        except DoesNotExist:
            return False

class DynamoDBOrderRepository(OrderRepository):
    async def create(self, order: Order) -> Order:
        order_model = OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            menu_id=order.menu_id,
            quantity=order.quantity,
            status=order.status.value,
            created_at=order.created_at
        )
        order_model.save()
        return order

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        try:
            item = OrderModel.get(order_id)
            return Order(
                id=item.id,
                customer_id=item.customer_id,
                menu_id=item.menu_id,
                quantity=item.quantity,
                status=OrderStatus(item.status),
                created_at=item.created_at,
                updated_at=item.updated_at
            )
        except DoesNotExist:
            return None

    async def update(self, order: Order) -> Order:
        order_model = OrderModel.get(order.id)
        order_model.status = order.status.value
        order_model.updated_at = datetime.utcnow()
        order_model.save()
        return order