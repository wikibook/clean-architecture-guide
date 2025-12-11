from abc import ABC, abstractmethod

from ..dtos.menu_dtos import MenuListResponseDTO, MenuResponseDTO
from ..repositories.menu_repository import MenuRepository


class GetMenuListUseCase(ABC):
    @abstractmethod
    def execute(self) -> MenuListResponseDTO:
        pass


class GetMenuListUseCaseImpl(GetMenuListUseCase):
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    def execute(self) -> MenuListResponseDTO:
        menus = self.menu_repository.get_all()
        menu_dtos = [
            MenuResponseDTO(
                menu_id=menu.menu_id,
                name=menu.name,
                price=menu.price,
                category=menu.category,
            )
            for menu in menus
        ]
        return MenuListResponseDTO(menus=menu_dtos)
