from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.menu import Menu


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
