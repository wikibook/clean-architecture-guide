from typing import Dict

from application.dtos import CreateOrderOutputDto
from application.ports.outbound import OutputBoundary


class CreateOrderPresenter(OutputBoundary):
    def __init__(self):
        self._result = None

    def set_result(self, output_dto: CreateOrderOutputDto) -> None:
        self._result = output_dto

    def present(self) -> Dict:
        if not self._result:
            return {"status": "error", "message": "No result to present"}

        return {
            "status": "success",
            "data": {
                "orderId": self._result.order_id,
                "customerId": self._result.customer_id,
                "totalAmount": self._result.total_amount,
                "currency": self._result.currency,
                "status": self._result.status,
                "items": self._result.items,
            },
            "message": "order created successfully",
        }
