from abc import ABC, abstractmethod
from typing import Optional

from ..dtos.customer_dtos import CustomerResponseDTO
from ..repositories.customer_repository import CustomerRepository


class GetCustomerUseCase(ABC):
    @abstractmethod
    def execute(self, customer_id: str) -> Optional[CustomerResponseDTO]:
        pass


class GetCustomerUseCaseImpl(GetCustomerUseCase):
    def __init__(self, customer_repository: CustomerRepository) -> None:
        self.customer_repository = customer_repository

    def execute(self, customer_id: str) -> Optional[CustomerResponseDTO]:
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            return None

        return CustomerResponseDTO(
            customer_id=customer.customer_id,
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
        )
