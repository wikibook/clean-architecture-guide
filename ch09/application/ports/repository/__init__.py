from abc import ABC, abstractmethod
from typing import Optional, List

from domain.entities.coffee import Coffee
from domain.entities.order import Order


class CoffeeRepository(ABC):
    @abstractmethod
    def find_by_id(self, coffee_id: str) -> Optional[Coffee]:
        pass

    @abstractmethod
    def find_all_available(self) -> List[Coffee]:
        pass

    @abstractmethod
    def save(self, coffee: Coffee) -> None:
        pass


class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass
