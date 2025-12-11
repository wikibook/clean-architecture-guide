from typing import Any

from fastapi import APIRouter, HTTPException

from ...domain.dtos.order_dtos import CreateOrderRequestDTO
from ...domain.usecases.order_usecases import (
    CreateOrderUseCase,
    DeleteOrderUseCase,
    GetOrderStatusUseCase,
)
from ..schemas.api_response import (
    APIResponse,
    CreateOrderRequest,
    DeleteOrderResponse,
    OrderResponse,
)


class OrderController:
    def __init__(
        self,
        create_order_usecase: CreateOrderUseCase,
        get_order_status_usecase: GetOrderStatusUseCase,
        delete_order_usecase: DeleteOrderUseCase,
    ) -> None:
        self.create_order_usecase = create_order_usecase
        self.get_order_status_usecase = get_order_status_usecase
        self.delete_order_usecase = delete_order_usecase
        self.router = APIRouter(tags=["order"])

    def _handle_create_order(
        self, request: CreateOrderRequest
    ) -> APIResponse[OrderResponse]:
        try:
            dto = CreateOrderRequestDTO(
                customer_id=request.customer_id,
                menu_id=request.menu_id,
                quantity=request.quantity,
                options=request.options,
            )
            result = self.create_order_usecase.execute(dto)
            return APIResponse[OrderResponse](
                status="success",
                data=OrderResponse(
                    order_id=result.order_id,
                    status=result.status,
                    created_at=result.created_at,
                ),
                message="Order created successfully",
            )
        except ValueError as e:
            if str(e) == "Invalid menu ID":
                raise HTTPException(status_code=404, detail=str(e)) from e
            elif str(e) == "Insufficient stock":
                raise HTTPException(status_code=400, detail=str(e)) from e
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def _handle_get_order_status(self, order_id: str) -> APIResponse[OrderResponse]:
        try:
            result = self.get_order_status_usecase.execute(order_id)
            if result is None:
                raise HTTPException(status_code=404, detail="Order not found")
            return APIResponse[OrderResponse](
                status="success",
                data=OrderResponse(
                    order_id=result.order_id,
                    status=result.status,
                    created_at=result.created_at,
                ),
                message="Order status retrieved successfully",
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def _handle_delete_order(self, order_id: str) -> APIResponse[DeleteOrderResponse]:
        try:
            # 먼저 주문이 존재하는지 확인
            order = self.get_order_status_usecase.execute(order_id)
            if order is None:
                raise HTTPException(status_code=404, detail="Order not found")

            result = self.delete_order_usecase.execute(order_id)
            if result is None:
                raise HTTPException(status_code=500, detail="Failed to delete order")

            return APIResponse[DeleteOrderResponse](
                status="success",
                data=DeleteOrderResponse(
                    order_id=result.order_id,
                    success=result.success,
                    message=result.message,
                ),
                message="Order deleted successfully",
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    def register_routes(self) -> APIRouter:
        @self.router.post("/order", response_model=APIResponse[OrderResponse])
        async def create_order(request: CreateOrderRequest) -> Any:
            return self._handle_create_order(request)

        @self.router.get("/order/{order_id}", response_model=APIResponse[OrderResponse])
        async def get_order_status(order_id: str) -> Any:
            return self._handle_get_order_status(order_id)

        @self.router.delete(
            "/order/{order_id}", response_model=APIResponse[DeleteOrderResponse]
        )
        async def delete_order(order_id: str) -> Any:
            return self._handle_delete_order(order_id)

        return self.router
