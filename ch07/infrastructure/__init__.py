from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class MenuItemModel(Model):
    class Meta:
        table_name = "MenuItems"
        region = "us-east-1"

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    price = NumberAttribute()
    description = UnicodeAttribute()
    stock = NumberAttribute()


class OrderModel(Model):
    class Meta:
        table_name = "Orders"
        region = "us-east-1"

    id = UnicodeAttribute(hash_key=True)
    customer_id = UnicodeAttribute()
    item_id = UnicodeAttribute(null=True)  # 단일 OrderItem ID
    total_amount = NumberAttribute()
    status = UnicodeAttribute()
    created_at = UnicodeAttribute()


class OrderItemModel(Model):
    class Meta:
        table_name = "OrderItems"
        region = "us-east-1"

    id = UnicodeAttribute(hash_key=True)
    order_id = UnicodeAttribute(range_key=True)
    menu_item_id = UnicodeAttribute()
    quantity = NumberAttribute()
    unit_price = NumberAttribute()
