from typing import List, Optional
from ...domain.entities.menu import Menu
from ...domain.entities.order import Order
from ...domain.interfaces.repositories import MenuRepository, OrderRepository
from .dynamodb_models import MenuModel, OrderModel


class DynamoDBMenuRepository(MenuRepository):
    def get_all(self) -> List[Menu]:
        return [
            Menu(
                menu_id=item.menu_id,
                name=item.name,
                price=item.price,
                category=item.category,
                stock=item.stock
            )
            for item in MenuModel.scan()
        ]
    
    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        try:
            item = MenuModel.get(menu_id)
            return Menu(
                menu_id=item.menu_id,
                name=item.name,
                price=item.price,
                category=item.category,
                stock=item.stock
            )
        except MenuModel.DoesNotExist:
            return None
    
    def update(self, menu: Menu) -> None:
        item = MenuModel(
            menu_id=menu.menu_id,
            name=menu.name,
            price=menu.price,
            category=menu.category,
            stock=menu.stock
        )
        item.save()


class DynamoDBOrderRepository(OrderRepository):
    def create(self, order: Order) -> None:
        item = OrderModel(
            order_id=order.order_id,
            customer_id=order.customer_id,
            menu_id=order.menu_id,
            quantity=order.quantity,
            status=order.status,
            options=order.options,
            created_at=order.created_at
        )
        item.save()
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        try:
            item = OrderModel.get(order_id)
            return Order(
                order_id=item.order_id,
                customer_id=item.customer_id,
                menu_id=item.menu_id,
                quantity=item.quantity,
                status=item.status,
                options=item.options,
                created_at=item.created_at
            )
        except OrderModel.DoesNotExist:
            return None
    
    def update(self, order: Order) -> None:
        item = OrderModel(
            order_id=order.order_id,
            customer_id=order.customer_id,
            menu_id=order.menu_id,
            quantity=order.quantity,
            status=order.status,
            options=order.options,
            created_at=order.created_at
        )
        item.save()