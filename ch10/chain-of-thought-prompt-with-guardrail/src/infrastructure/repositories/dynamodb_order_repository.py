from typing import Optional

from pynamodb.attributes import (
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.models import Model

from ...domain.entities.order import Order
from ...domain.repositories.order_repository import OrderRepository


class OrderModel(Model):
    class Meta:
        table_name = "orders"
        region = "ap-northeast-2"

    order_id = UnicodeAttribute(hash_key=True)
    customer_id = UnicodeAttribute()
    menu_id = UnicodeAttribute()
    quantity = NumberAttribute()
    status = UnicodeAttribute()
    options = MapAttribute()
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute(null=True)


class DynamoDBOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        item = OrderModel(
            order_id=order.order_id,
            customer_id=order.customer_id,
            menu_id=order.menu_id,
            quantity=order.quantity,
            status=order.status,
            options=order.options,
            created_at=order.created_at,
            updated_at=order.updated_at,
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
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
        except OrderModel.DoesNotExist:
            return None
