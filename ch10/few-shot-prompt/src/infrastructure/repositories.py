from typing import List, Optional
from pynamodb.exceptions import DoesNotExist, PutError
from datetime import datetime

from src.domain.entities import Menu, Order, MenuCategory, OrderStatus
from src.domain.repositories import MenuRepository, OrderRepository
from .models import MenuModel, OrderModel


class DynamoDBMenuRepository(MenuRepository):
    async def get_all(self) -> List[Menu]:
        try:
            menu_models = MenuModel.scan()
            return [
                Menu(
                    menu_id=m.menu_id,
                    name=m.name,
                    price=m.price,
                    category=MenuCategory(m.category),
                    stock=m.stock,
                )
                for m in menu_models
            ]
        except Exception as e:
            raise Exception(f"Failed to get menus: {str(e)}")

    async def get_by_id(self, menu_id: str) -> Optional[Menu]:
        try:
            menu = MenuModel.get(menu_id)
            return Menu(
                menu_id=menu.menu_id,
                name=menu.name,
                price=menu.price,
                category=MenuCategory(menu.category),
                stock=menu.stock,
            )
        except DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Failed to get menu: {str(e)}")

    async def update_stock(self, menu_id: str, quantity: int) -> bool:
        try:
            menu = await self.get_by_id(menu_id)
            if not menu or menu.stock < abs(quantity):
                return False
            
            menu_model = MenuModel.get(menu_id)
            menu_model.stock = menu.stock + quantity
            menu_model.save()
            return True
        except Exception as e:
            raise Exception(f"Failed to update stock: {str(e)}")


class DynamoDBOrderRepository(OrderRepository):
    async def create(self, order: Order) -> Order:
        try:
            order_model = OrderModel(
                order_id=order.order_id,
                customer_id=order.customer_id,
                menu_id=order.menu_id,
                quantity=order.quantity,
                options={
                    "size": order.options.size,
                    "temperature": order.options.temperature,
                },
                status=order.status.value,
                created_at=order.created_at,
            )
            order_model.save()
            return order
        except PutError as e:
            raise Exception(f"Failed to create order: {str(e)}")

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        try:
            order = OrderModel.get(order_id)
            return Order(
                order_id=order.order_id,
                customer_id=order.customer_id,
                menu_id=order.menu_id,
                quantity=order.quantity,
                options=order.options,
                status=OrderStatus(order.status),
                created_at=order.created_at,
            )
        except DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Failed to get order: {str(e)}")

    async def update_status(self, order_id: str, status: str) -> bool:
        try:
            order = OrderModel.get(order_id)
            order.status = status
            order.save()
            return True
        except DoesNotExist:
            return False
        except Exception as e:
            raise Exception(f"Failed to update order status: {str(e)}")