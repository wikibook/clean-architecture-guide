from typing import Optional

from sqlalchemy.orm import Session

from ...domain.entities.order import Order
from ...domain.repositories.order_repository import OrderRepository
from ..database.models.order import OrderModel


class MySQLOrderRepository(OrderRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def save(self, order: Order) -> None:
        order_model = OrderModel(
            order_id=order.order_id,
            customer_id=order.customer_id,
            menu_id=order.menu_id,
            quantity=order.quantity,
            status=order.status,
            options=order.options,
        )
        self.db.add(order_model)
        self.db.commit()

    def get_by_id(self, order_id: str) -> Optional[Order]:
        order_model = (
            self.db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
        )
        if not order_model:
            return None

        return Order(
            order_id=order_model.order_id,
            customer_id=order_model.customer_id,
            menu_id=order_model.menu_id,
            quantity=order_model.quantity,
            status=order_model.status,
            options=order_model.options,
            created_at=order_model.created_at,
            updated_at=order_model.updated_at,
        )

    def delete(self, order_id: str) -> bool:
        try:
            result: int = (
                self.db.query(OrderModel)
                .filter(OrderModel.order_id == order_id)
                .delete()
            )
            self.db.commit()
            return result > 0
        except Exception:
            self.db.rollback()
            return False
