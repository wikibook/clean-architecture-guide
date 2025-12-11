from fastapi import APIRouter, HTTPException

from ...domain.usecases.menu_usecases import GetMenuListUseCase
from ..schemas.api_response import APIResponse, MenuListResponse


class MenuController:
    def __init__(self, get_menu_list_usecase: GetMenuListUseCase) -> None:
        self.get_menu_list_usecase = get_menu_list_usecase
        self.router = APIRouter(tags=["menu"])

    def register_routes(self) -> APIRouter:
        @self.router.get("/menu", response_model=APIResponse[MenuListResponse])
        async def get_menu_list() -> APIResponse[MenuListResponse]:
            try:
                result = self.get_menu_list_usecase.execute()
                return APIResponse(
                    status="success",
                    message="Menus retrieved successfully",
                    data=MenuListResponse(
                        menus=[
                            {
                                "menu_id": menu.menu_id,
                                "name": menu.name,
                                "price": menu.price,
                                "category": menu.category,
                            }
                            for menu in result.menus
                        ]
                    ),
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=str(e),
                ) from e

        return self.router
