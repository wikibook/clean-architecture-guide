from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.menu import Menu
from ..entities.order import Order


class MenuRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Menu]:
        pass
    
    @abstractmethod
    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        pass
    
    @abstractmethod
    def update(self, menu: Menu) -> None:
        pass


class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def update(self, order: Order) -> None:
        pass