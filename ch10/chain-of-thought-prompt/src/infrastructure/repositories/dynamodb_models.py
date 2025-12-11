from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, 
    UTCDateTimeAttribute, MapAttribute
)
from datetime import datetime

class MenuModel(Model):
    class Meta:
        table_name = 'menus'
        region = 'ap-northeast-2'

    menu_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    price = NumberAttribute()
    category = UnicodeAttribute()
    stock = NumberAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.utcnow)
    updated_at = UTCDateTimeAttribute(default=datetime.utcnow)

class OrderModel(Model):
    class Meta:
        table_name = 'orders'
        region = 'ap-northeast-2'

    order_id = UnicodeAttribute(hash_key=True)
    customer_id = UnicodeAttribute()
    menu_id = UnicodeAttribute()
    quantity = NumberAttribute()
    status = UnicodeAttribute()
    options = MapAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.utcnow)
    updated_at = UTCDateTimeAttribute(default=datetime.utcnow)