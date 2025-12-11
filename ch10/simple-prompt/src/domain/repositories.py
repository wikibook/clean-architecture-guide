from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Menu, Order

class MenuRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Menu]:
        pass

    @abstractmethod
    async def get_by_id(self, menu_id: str) -> Optional[Menu]:
        pass

    @abstractmethod
    async def update_stock(self, menu_id: str, quantity: int) -> bool:
        pass

class OrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        pass