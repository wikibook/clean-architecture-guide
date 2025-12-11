from typing import List
from ..interfaces.boundaries import MenuInputBoundary, MenuOutputDTO
from ..interfaces.repositories import MenuRepository

class MenuUseCases(MenuInputBoundary):
    def __init__(self, menu_repository: MenuRepository):
        self._menu_repository = menu_repository

    def get_all_menus(self) -> List[MenuOutputDTO]:
        """모든 메뉴 조회"""
        menus = self._menu_repository.get_all()
        return [
            MenuOutputDTO(
                menu_id=menu.menu_id,
                name=menu.name,
                price=menu.price,
                category=menu.category
            )
            for menu in menus
        ]