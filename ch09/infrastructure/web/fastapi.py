import json
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mangum import Mangum

from application.dtos import CreateOrderInputDto
from application.usecases.create_order_usecase import CreateOrderUseCase
from adapter.repository import DynamoDBCoffeeRepository, DynamoDBOrderRepository
import os
from adapter.events import InMemoryEventBus
from adapter.events.payment_subscriber import subscribe_payment_handlers
from adapter.gateway import InMemoryPaymentGateway
from application.usecases.process_payment_usecase import ProcessPaymentUseCase
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
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    if sns_topic_arn:
        # 지연 import로 테스트 환경에서의 의존성 문제를 피합니다
        from adapter.events.sns_publisher import SnsDomainEventPublisher  # type: ignore

        publisher = SnsDomainEventPublisher()
        return CreateOrderUseCase(presenter, coffee_repo, order_repo, event_publisher=publisher)
    else:
        # 로컬/테스트 환경: 인메모리 버스 사용 + 결제 구독자 연결
        bus = InMemoryEventBus()
        payment_gateway = InMemoryPaymentGateway()
        payment_usecase = ProcessPaymentUseCase(order_repo=order_repo, payment_gateway=payment_gateway)
        subscribe_payment_handlers(bus, order_repo, payment_usecase)
        return CreateOrderUseCase(presenter, coffee_repo, order_repo, event_publisher=bus)


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


handler = Mangum(app)
