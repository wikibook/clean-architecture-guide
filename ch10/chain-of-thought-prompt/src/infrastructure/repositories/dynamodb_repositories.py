from typing import List, Optional
from datetime import datetime
from ...domain.entities.menu import Menu
from ...domain.entities.order import Order, OrderStatus
from ...domain.interfaces.repositories import MenuRepository, OrderRepository
from .dynamodb_models import MenuModel, OrderModel

class DynamoDBMenuRepository(MenuRepository):
    def get_all(self) -> List[Menu]:
        """모든 메뉴 조회"""
        try:
            menu_models = MenuModel.scan()
            return [
                Menu(
                    menu_id=m.menu_id,
                    name=m.name,
                    price=m.price,
                    category=m.category,
                    stock=m.stock,
                    created_at=m.created_at,
                    updated_at=m.updated_at
                )
                for m in menu_models
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        """ID로 메뉴 조회"""
        try:
            menu = MenuModel.get(menu_id)
            return Menu(
                menu_id=menu.menu_id,
                name=menu.name,
                price=menu.price,
                category=menu.category,
                stock=menu.stock,
                created_at=menu.created_at,
                updated_at=menu.updated_at
            )
        except MenuModel.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def update(self, menu: Menu) -> None:
        """메뉴 정보 업데이트"""
        try:
            menu_model = MenuModel.get(menu.menu_id)
            menu_model.stock = menu.stock
            menu_model.updated_at = datetime.utcnow()
            menu_model.save()
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

class DynamoDBOrderRepository(OrderRepository):
    def create(self, order: Order) -> None:
        """주문 생성"""
        try:
            order_model = OrderModel(
                order_id=order.order_id,
                customer_id=order.customer_id,
                menu_id=order.menu_id,
                quantity=order.quantity,
                status=order.status.name,
                options=order.options,
                created_at=order.created_at,
                updated_at=order.updated_at
            )
            order_model.save()
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def get_by_id(self, order_id: str) -> Optional[Order]:
        """ID로 주문 조회"""
        try:
            order = OrderModel.get(order_id)
            return Order(
                order_id=order.order_id,
                customer_id=order.customer_id,
                menu_id=order.menu_id,
                quantity=order.quantity,
                status=OrderStatus[order.status],
                options=order.options,
                created_at=order.created_at,
                updated_at=order.updated_at
            )
        except OrderModel.DoesNotExist:
            return None
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

    def update(self, order: Order) -> None:
        """주문 정보 업데이트"""
        try:
            order_model = OrderModel.get(order.order_id)
            order_model.status = order.status.name
            order_model.updated_at = datetime.utcnow()
            order_model.save()
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")