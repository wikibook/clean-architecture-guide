import json
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mangum import Mangum

from application.dtos import CreateOrderInputDto
from application.usecases.create_order_usecase import CreateOrderUseCase
from adapter.repository import DynamoDBCoffeeRepository, DynamoDBOrderRepository
from adapter.presenter.create_order_presenter import CreateOrderPresenter
from domain.exceptions import OnlineCafeException

app = FastAPI()


class OrderRequest(BaseModel):
    customer_id: str
    coffee_id: str
    quantity: int


def get_create_order_use_case() -> CreateOrderUseCase:
    presenter = CreateOrderPresenter()
    coffee_repo = DynamoDBCoffeeRepository()
    order_repo = DynamoDBOrderRepository()

    return CreateOrderUseCase(presenter, coffee_repo, order_repo)


@app.post("/order")
def create_order(request: OrderRequest, usecase: CreateOrderUseCase = Depends(get_create_order_use_case)):
    try:
        input_dto = CreateOrderInputDto(request.customer_id, request.coffee_id, request.quantity)
        usecase.execute(input_dto)
        return JSONResponse(status_code=200, content=usecase.output_boundary.present())
    except OnlineCafeException as e:
        return JSONResponse(status_code=e.get_status_code(), content=json.loads(e.get_response_body()))
    except Exception:
        return JSONResponse(status_code=500, content="Internal Server Error")


@app.get("/test")
def hello_world():
    return {"status": "success", "data": {"message": "Hello, World!"}}


handler = Mangum(app)
