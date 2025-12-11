from typing import List
from ..interfaces.boundaries import GetMenusInputBoundary, MenuOutputDTO
from ..interfaces.repositories import MenuRepository


class GetMenusUseCase(GetMenusInputBoundary):
    def __init__(self, menu_repository: MenuRepository):
        self._menu_repository = menu_repository

    def execute(self) -> List[MenuOutputDTO]:
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