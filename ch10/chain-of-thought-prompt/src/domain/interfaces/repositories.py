from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.menu import Menu
from ..entities.order import Order

class MenuRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Menu]:
        """모든 메뉴 조회"""
        pass

    @abstractmethod
    def get_by_id(self, menu_id: str) -> Optional[Menu]:
        """ID로 메뉴 조회"""
        pass

    @abstractmethod
    def update(self, menu: Menu) -> None:
        """메뉴 정보 업데이트"""
        pass

class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> None:
        """주문 생성"""
        pass

    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        """ID로 주문 조회"""
        pass

    @abstractmethod
    def update(self, order: Order) -> None:
        """주문 정보 업데이트"""
        pass