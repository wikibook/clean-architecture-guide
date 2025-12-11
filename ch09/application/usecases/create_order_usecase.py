import datetime

from application.dtos import CreateOrderInputDto, CreateOrderOutputDto
from application.ports.inbound import CreateOrderInputBoundary
from application.ports.outbound import OutputBoundary, DomainEventPublisher
from application.ports.repository import CoffeeRepository, OrderRepository
from domain.entities.order import Order
from domain.exceptions import InvalidInputParameter


class CreateOrderUseCase(CreateOrderInputBoundary):
    def __init__(
        self,
        output_boundary: OutputBoundary,
        coffee_repo: CoffeeRepository,
        order_repo: OrderRepository,
        event_publisher: DomainEventPublisher | None = None,
    ):
        self.output_boundary = output_boundary
        self.coffee_repo = coffee_repo
        self.order_repo = order_repo
        self.event_publisher = event_publisher

    def execute(self, input_dto: CreateOrderInputDto) -> None:
        coffee = self.coffee_repo.find_by_id(input_dto.coffee_id)
        if not coffee or not coffee.is_available():
            raise InvalidInputParameter("주문 불가능한 커피입니다")

        order_id = f"order-{input_dto.customer_id}-{int(datetime.datetime.now().timestamp())}"
        order = Order(id=order_id, customer_id=input_dto.customer_id)
        order.add_coffee(coffee, input_dto.quantity)

        # 주문과 커피 정보 저장
        self.order_repo.save(order)
        self.coffee_repo.save(coffee)

        # 도메인 이벤트 발행 (있다면)
        if self.event_publisher is not None:
            self.event_publisher.publish_all(order.pull_domain_events())

        # 출력 DTO 생성
        items = []
        for item in order.items:
            items.append(
                {
                    "id": item.id,
                    "coffee_id": item.coffee_id,
                    "quantity": item.quantity,
                    "unit_price": str(item.unit_price),
                    "subtotal": str(item.calculate_subtotal()),
                }
            )

        output_dto = CreateOrderOutputDto(
            order_id=order.id,
            customer_id=order.customer_id,
            total_amount=order.total_amount.amount,
            currency=order.total_amount.currency,
            status=order.status.value,
            items=items,
        )

        self.output_boundary.set_result(output_dto)
