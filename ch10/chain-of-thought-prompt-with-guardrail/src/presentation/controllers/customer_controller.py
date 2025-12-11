from fastapi import APIRouter, HTTPException

from ...domain.usecases.customer_usecases import GetCustomerUseCase
from ..schemas.api_response import APIResponse, CustomerResponse


class CustomerController:
    def __init__(self, get_customer_usecase: GetCustomerUseCase) -> None:
        self.get_customer_usecase = get_customer_usecase
        self.router = APIRouter(tags=["customer"])

    def register_routes(self) -> APIRouter:
        @self.router.get(
            "/customer/{customer_id}",
            response_model=APIResponse[CustomerResponse],
        )
        async def get_customer(customer_id: str) -> APIResponse[CustomerResponse]:
            try:
                result = self.get_customer_usecase.execute(customer_id)
                if not result:
                    raise HTTPException(
                        status_code=404,
                        detail="Customer not found",
                    ) from None
                return APIResponse(
                    status="success",
                    message="Customer retrieved successfully",
                    data=CustomerResponse(
                        customer_id=result.customer_id,
                        name=result.name,
                        email=result.email,
                        phone=result.phone,
                        created_at=result.created_at,
                        updated_at=result.updated_at,
                    ),
                )
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=str(e),
                ) from e

        return self.router
