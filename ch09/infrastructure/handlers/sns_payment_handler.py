import json
from typing import Any, Dict

from adapter.repository import DynamoDBOrderRepository
from adapter.gateway import InMemoryPaymentGateway
from application.usecases.process_payment_usecase import ProcessPaymentUseCase


def handler(event: Dict[str, Any], _context: Any) -> None:
    """SNS 구독 람다 핸들러

    - SNS 메시지를 수신하여 `OrderCreated` 이벤트를 식별합니다.
    - 결제 유스케이스를 호출하여 결제 승인/실패에 따른 주문 상태를 갱신합니다.
    """

    order_repo = DynamoDBOrderRepository()
    payment_gateway = InMemoryPaymentGateway()  # 데모용: 항상 승인
    usecase = ProcessPaymentUseCase(order_repo=order_repo, payment_gateway=payment_gateway)

    for record in event.get("Records", []):
        message_str = record.get("Sns", {}).get("Message")
        if not message_str:
            continue
        try:
            message = json.loads(message_str)
        except json.JSONDecodeError:
            continue

        name = message.get("name")
        payload = message.get("payload", {})

        if name == "OrderCreated":
            order_id = payload.get("order_id")
            if order_id:
                usecase.execute(order_id)

