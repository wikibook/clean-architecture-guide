from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
from datetime import datetime

class MenuModel(Model):
    class Meta:
        table_name = 'Menu'
        region = 'ap-northeast-2'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    price = NumberAttribute()
    category = UnicodeAttribute()
    stock = NumberAttribute()

class OrderModel(Model):
    class Meta:
        table_name = 'Order'
        region = 'ap-northeast-2'

    id = UnicodeAttribute(hash_key=True)
    customer_id = UnicodeAttribute()
    menu_id = UnicodeAttribute()
    quantity = NumberAttribute()
    status = UnicodeAttribute()
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute(null=True)