from typing import Optional

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from ...domain.entities.customer import Customer
from ...domain.repositories.customer_repository import CustomerRepository


class CustomerModel(Model):
    class Meta:
        table_name = "customers"
        region = "ap-northeast-2"

    customer_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    email = UnicodeAttribute()
    phone = UnicodeAttribute()
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute(null=True)


class DynamoDBCustomerRepository(CustomerRepository):
    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        try:
            item = CustomerModel.get(customer_id)
            return Customer(
                customer_id=item.customer_id,
                name=item.name,
                email=item.email,
                phone=item.phone,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
        except CustomerModel.DoesNotExist:
            return None
