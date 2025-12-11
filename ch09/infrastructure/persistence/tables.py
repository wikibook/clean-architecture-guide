from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class CoffeeModel(Model):
    class Meta:
        table_name = "Coffees"
        region = "ap-northeast-2"

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    price = NumberAttribute()
    currency = UnicodeAttribute(default="KRW")
    description = UnicodeAttribute(null=True)
    stock = NumberAttribute()


class OrderItemModel(Model):
    class Meta:
        table_name = "OrderItems"
        region = "ap-northeast-2"

    id = UnicodeAttribute(hash_key=True)
    order_id = UnicodeAttribute()
    coffee_id = UnicodeAttribute()
    quantity = NumberAttribute()
    unit_price = NumberAttribute()
    currency = UnicodeAttribute(default="KRW")


class OrderModel(Model):
    class Meta:
        table_name = "Orders"
        region = "ap-northeast-2"

    id = UnicodeAttribute(hash_key=True)
    customer_id = UnicodeAttribute()
    total_amount = NumberAttribute()
    currency = UnicodeAttribute(default="KRW")
    status = UnicodeAttribute()
    created_at = UnicodeAttribute()
