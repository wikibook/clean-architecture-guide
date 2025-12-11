from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ...domain.interfaces.boundaries import (
    MenuInputBoundary, OutputBoundary
)

router = APIRouter()

class MenuController:
    def __init__(
        self,
        menu_usecase: MenuInputBoundary,
        presenter: OutputBoundary
    ):
        self.menu_usecase = menu_usecase
        self.presenter = presenter

    def register_routes(self, router: APIRouter) -> None:
        """라우트 등록"""
        router.add_api_route(
            "/menu",
            self.get_menus,
            methods=["GET"],
            response_model=Dict[str, Any]
        )

    async def get_menus(self) -> Dict[str, Any]:
        """메뉴 목록 조회"""
        try:
            menus = self.menu_usecase.get_all_menus()
            response = self.presenter.present_success(
                data=menus,
                message="Menus retrieved successfully"
            )
            return response.__dict__
        except Exception as e:
            response = self.presenter.present_error(
                message=str(e)
            )
            raise HTTPException(
                status_code=500,
                detail=response.__dict__
            )