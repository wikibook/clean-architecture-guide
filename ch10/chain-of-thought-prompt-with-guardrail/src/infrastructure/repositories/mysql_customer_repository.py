from typing import Optional

from sqlalchemy.orm import Session

from ...domain.entities.customer import Customer
from ...domain.repositories.customer_repository import CustomerRepository
from ..database.models.customer import CustomerModel


class MySQLCustomerRepository(CustomerRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        customer_model = (
            self.db.query(CustomerModel)
            .filter(CustomerModel.customer_id == customer_id)
            .first()
        )
        if not customer_model:
            return None

        return Customer(
            customer_id=customer_model.customer_id,
            name=customer_model.name,
            email=customer_model.email,
            phone=customer_model.phone,
            created_at=customer_model.created_at,
            updated_at=customer_model.updated_at,
        )
