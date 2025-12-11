from fastapi import APIRouter, HTTPException
from ...domain.interfaces.boundaries import GetMenusInputBoundary, OutputBoundary

router = APIRouter()


class MenuController:
    def __init__(
        self,
        get_menus_usecase: GetMenusInputBoundary,
        presenter: OutputBoundary
    ):
        self._get_menus_usecase = get_menus_usecase
        self._presenter = presenter
        
    async def get_menus(self):
        try:
            menus = self._get_menus_usecase.execute()
            return self._presenter.present_success(
                data=menus,
                message="Menus retrieved successfully"
            )
        except Exception as e:
            return self._presenter.present_error(
                message="Database error occurred"
            )