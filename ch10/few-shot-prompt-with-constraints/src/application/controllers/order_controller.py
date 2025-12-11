from fastapi import APIRouter, HTTPException
from ...domain.interfaces.boundaries import (
    CreateOrderInputBoundary, GetOrderInputBoundary,
    CreateOrderInputDTO, GetOrderInputDTO, OutputBoundary
)

router = APIRouter()


class OrderController:
    def __init__(
        self,
        create_order_usecase: CreateOrderInputBoundary,
        get_order_usecase: GetOrderInputBoundary,
        presenter: OutputBoundary
    ):
        self._create_order_usecase = create_order_usecase
        self._get_order_usecase = get_order_usecase
        self._presenter = presenter
    
    async def create_order(self, customer_id: str, menu_id: str, quantity: int, options: dict):
        try:
            input_dto = CreateOrderInputDTO(
                customer_id=customer_id,
                menu_id=menu_id,
                quantity=quantity,
                options=options
            )
            order = self._create_order_usecase.execute(input_dto)
            return self._presenter.present_success(
                data=order,
                message="Order created successfully"
            )
        except ValueError as e:
            if str(e) == "Invalid menu ID":
                return self._presenter.present_error(
                    message="Invalid menu ID"
                )
            elif str(e) == "Insufficient stock":
                return self._presenter.present_error(
                    message="Insufficient stock"
                )
            return self._presenter.present_error(
                message=str(e)
            )
        except Exception as e:
            return self._presenter.present_error(
                message="An error occurred while creating the order"
            )
    
    async def get_order(self, order_id: str):
        try:
            input_dto = GetOrderInputDTO(order_id=order_id)
            order = self._get_order_usecase.execute(input_dto)
            return self._presenter.present_success(
                data=order,
                message="Order status retrieved successfully"
            )
        except ValueError as e:
            if str(e) == "Order not found":
                return self._presenter.present_error(
                    message="Order not found"
                )
            return self._presenter.present_error(
                message=str(e)
            )
        except Exception as e:
            return self._presenter.present_error(
                message="An error occurred while retrieving the order"
            )