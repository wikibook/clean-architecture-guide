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
        """
        메뉴의 재고를 업데이트합니다.
        
        Args:
            menu_id: 메뉴 ID
            quantity: 차감할 수량 (음수)
            
        Returns:
            bool: 재고 업데이트 성공 여부
        """
        pass


class OrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    async def update_status(self, order_id: str, status: str) -> bool:
        pass