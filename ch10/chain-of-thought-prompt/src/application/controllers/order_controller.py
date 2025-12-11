from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ...domain.interfaces.boundaries import (
    OrderInputBoundary, OutputBoundary,
    CreateOrderInputDTO, GetOrderInputDTO
)

router = APIRouter()

class OrderController:
    def __init__(
        self,
        order_usecase: OrderInputBoundary,
        presenter: OutputBoundary
    ):
        self.order_usecase = order_usecase
        self.presenter = presenter

    def register_routes(self, router: APIRouter) -> None:
        """라우트 등록"""
        router.add_api_route(
            "/order",
            self.create_order,
            methods=["POST"],
            response_model=Dict[str, Any]
        )
        router.add_api_route(
            "/order/{order_id}",
            self.get_order,
            methods=["GET"],
            response_model=Dict[str, Any]
        )

    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """주문 생성"""
        try:
            input_dto = CreateOrderInputDTO(
                customer_id=order_data["customer_id"],
                menu_id=order_data["menu_id"],
                quantity=order_data["quantity"],
                options=order_data.get("options", {})
            )
            order = self.order_usecase.create_order(input_dto)
            response = self.presenter.present_success(
                data=order,
                message="Order created successfully"
            )
            return response.__dict__
        except ValueError as e:
            response = self.presenter.present_error(
                message=str(e)
            )
            raise HTTPException(
                status_code=400,
                detail=response.__dict__
            )
        except Exception as e:
            response = self.presenter.present_error(
                message=str(e)
            )
            raise HTTPException(
                status_code=500,
                detail=response.__dict__
            )

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        """주문 조회"""
        try:
            input_dto = GetOrderInputDTO(order_id=order_id)
            order = self.order_usecase.get_order(input_dto)
            response = self.presenter.present_success(
                data=order,
                message="Order status retrieved successfully"
            )
            return response.__dict__
        except ValueError as e:
            response = self.presenter.present_error(
                message=str(e)
            )
            raise HTTPException(
                status_code=404,
                detail=response.__dict__
            )
        except Exception as e:
            response = self.presenter.present_error(
                message=str(e)
            )
            raise HTTPException(
                status_code=500,
                detail=response.__dict__
            )