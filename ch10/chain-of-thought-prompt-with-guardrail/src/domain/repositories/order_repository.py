from abc import ABC, abstractmethod
from typing import Optional

from ..entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass

    @abstractmethod
    def delete(self, order_id: str) -> bool:
        """주문을 삭제합니다.

        Args:
            order_id: 삭제할 주문의 ID

        Returns:
            bool: 삭제 성공 여부
        """
        pass
