from abc import ABC, abstractmethod
from typing import Optional

from ..entities.customer import Customer


class CustomerRepository(ABC):
    @abstractmethod
    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        pass
